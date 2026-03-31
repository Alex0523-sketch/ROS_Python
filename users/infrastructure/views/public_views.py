import uuid
import unicodedata
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from users.infrastructure.models import UserModel
from users.infrastructure.models import HorarioModel
from users.infrastructure.models.promocion_model import PromocionModel
from users.infrastructure.models.noticia_model import NoticiaModel
from users.infrastructure.models.categoria_model import CategoriaModel
from users.infrastructure.models.producto_model import ProductoModel
from users.infrastructure.models.mesa_model import MesaModel
from users.infrastructure.models.reserva_model import ReservaModel
from users.infrastructure.models.pedido_model import PedidoModel
from users.infrastructure.models.detalle_pedido_model import DetallePedidoModel
from users.infrastructure.models.pago_model import PagoModel
from users.context_processors import SESSION_CARRITO_KEY
from users.utils.money import format_money_display

_CANCELADAS = ('CANCELADO', 'CANCELADA')

def _obtener_mesero_para_asignar():
    """
    Selecciona un empleado para asignar el pedido.
    Prioridad: empleados con horario activo en este momento.
    Fallback: si no hay horarios activos, asigna el que tenga menos pedidos pendientes.
    """
    def _normalize_day_str(val: str) -> str:
        raw = (val or '').strip().upper()
        # Quita tildes/acentos para comparar (ej: "MIÉRCOLES" == "MIERCOLES").
        raw = unicodedata.normalize('NFD', raw)
        raw = ''.join(ch for ch in raw if unicodedata.category(ch) != 'Mn')
        return raw

    now = timezone.localtime(timezone.now())
    # Mapeo estable (evita depender de locale del SO).
    weekday_map = {
        0: 'LUNES',
        1: 'MARTES',
        2: 'MIERCOLES',
        3: 'JUEVES',
        4: 'VIERNES',
        5: 'SABADO',
        6: 'DOMINGO',
    }
    today_day_norm = weekday_map.get(now.weekday())

    empleados = (
        UserModel.objects.filter(activo=True, rol__nombre__iexact='EMPLEADO')
        .select_related('rol')
        .order_by('id_user')
    )
    if not empleados.exists():
        return None

    # Filtra empleados por horario activo.
    horarios = HorarioModel.objects.filter(user__in=empleados).select_related('user')
    disponibles_ids = set()
    t_now = now.time()
    for h in horarios:
        if today_day_norm is None:
            break
        if _normalize_day_str(h.dia_semana) != today_day_norm:
            continue

        try:
            start_t = datetime.strptime((h.hora_inicio or '').strip(), '%H:%M').time()
            end_t = datetime.strptime((h.hora_fin or '').strip(), '%H:%M').time()
        except ValueError:
            continue

        if start_t <= end_t:
            activo = start_t <= t_now <= end_t
        else:
            # Soporta rangos nocturnos (ej: 22:00 - 02:00).
            activo = t_now >= start_t or t_now <= end_t

        if activo and h.user_id:
            disponibles_ids.add(h.user_id)

    candidatos = empleados
    if disponibles_ids:
        candidatos = empleados.filter(pk__in=disponibles_ids)

    # Elegimos el empleado con menos pedidos activos (no entregados/cancelados).
    mejor = None
    mejor_cantidad = None
    for emp in candidatos:
        pendientes = (
            PedidoModel.objects.filter(empleado_asignado=emp)
            .exclude(estado__iexact='ENTREGADO')
            .exclude(estado__in=_CANCELADAS)
            .count()
        )
        if mejor_cantidad is None or pendientes < mejor_cantidad:
            mejor = emp
            mejor_cantidad = pendientes
    return mejor


def _rol_upper_public(user):
    r = getattr(user, 'rol', None)
    raw = (r.nombre or '').strip().upper() if r else ''
    if raw in ('ADMIN', 'ADMINISTRADOR'):
        return 'ADMINISTRADOR'
    return raw


def index_view(request):
    today = timezone.localdate()
    promos_vigentes = PromocionModel.objects.filter(
        fecha_inicio__lte=today,
        fecha_fin__gte=today,
    ).order_by('-fecha_inicio', '-descuento')
    promocion_del_dia = promos_vigentes.first()
    if promocion_del_dia is None:
        promocion_del_dia = PromocionModel.objects.order_by(
            '-fecha_fin', '-fecha_inicio'
        ).first()
    if promos_vigentes.exists():
        promociones = promos_vigentes
    else:
        promociones = PromocionModel.objects.order_by('-fecha_inicio')[:6]
    noticias = NoticiaModel.objects.all().order_by('-fecha_publicacion')[:6]
    return render(request, 'public/index.html', {
        'promociones': promociones,
        'noticias': noticias,
        'promocion_del_dia': promocion_del_dia,
    })


def noticias_view(request):
    noticias = NoticiaModel.objects.all().order_by('-fecha_publicacion')
    return render(request, 'public/noticias.html', {'noticias': noticias})


def menu_view(request):
    categorias = CategoriaModel.objects.all().order_by('nombre')
    productos_qs = ProductoModel.objects.select_related('categoria').all().order_by(
        'categoria__nombre', 'nombre'
    )
    raw_cat = request.GET.get('categoria')
    categoria_seleccionada = None
    if raw_cat:
        try:
            categoria_seleccionada = int(raw_cat)
        except (TypeError, ValueError):
            categoria_seleccionada = None
    if categoria_seleccionada is not None:
        productos = productos_qs.filter(categoria_id=categoria_seleccionada)
    else:
        productos = productos_qs
    return render(request, 'public/menu.html', {
        'categorias': categorias,
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,
    })


def _parse_reserva_datetime(date_str: str, time_str: str):
    naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    if settings.USE_TZ:
        return timezone.make_aware(naive, timezone.get_current_timezone())
    return naive


def _mesa_ids_ocupadas_para_slot(fecha_reserva, hora_str: str):
    return set(
        ReservaModel.objects.filter(
            fecha_reserva=fecha_reserva,
            hora=hora_str,
        ).exclude(estado__in=_CANCELADAS).values_list('mesa_id', flat=True)
    )


def reserva_view(request):
    return render(request, 'public/reserva.html')


@require_http_methods(['GET', 'HEAD'])
def reserva_confirmada_view(request):
    codigo = request.GET.get('codigo', '')
    return render(request, 'public/reserva-confirmada.html', {'codigo': codigo})


@require_GET
def api_mesas_disponibilidad(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    if not fecha or not hora:
        return JsonResponse({'error': 'fecha y hora requeridos'}, status=400)
    try:
        fecha_reserva = _parse_reserva_datetime(fecha, hora)
    except ValueError:
        return JsonResponse({'error': 'fecha u hora inválida'}, status=400)

    ocupadas = _mesa_ids_ocupadas_para_slot(fecha_reserva, hora)
    disponibles = []
    reservadas = []
    for m in MesaModel.objects.all().order_by('numero_mesa'):
        if m.id_mesa in ocupadas:
            reservadas.append({'numeroMesa': m.numero_mesa, 'capacidad': m.capacidad})
        else:
            disponibles.append({'numeroMesa': m.numero_mesa, 'capacidad': m.capacidad})
    return JsonResponse({
        'totalDisponibles': len(disponibles),
        'disponibles': disponibles,
        'reservadas': reservadas,
    })


@require_http_methods(['POST'])
def reserva_crear_view(request):
    nombre = (request.POST.get('nombre') or '').strip()
    telefono = (request.POST.get('telefono') or '').strip()
    email = (request.POST.get('email') or '').strip()
    fecha_str = request.POST.get('fecha')
    hora = request.POST.get('hora')
    comentarios = (request.POST.get('comentarios') or '').strip() or None

    try:
        personas = int(request.POST.get('personas'))
    except (TypeError, ValueError):
        personas = 0

    if len(nombre) < 3 or any(c.isdigit() for c in nombre) or not telefono.isdigit() or len(telefono) < 7 or not email or not fecha_str or not hora:
        messages.error(request, 'Completa todos los campos correctamente.')
        return redirect('reserva')

    if personas < 1 or personas > 8:
        messages.error(request, 'El número de personas debe estar entre 1 y 8.')
        return redirect('reserva')

    try:
        fecha_reserva = _parse_reserva_datetime(fecha_str, hora)
    except ValueError:
        messages.error(request, 'Fecha u hora no válida.')
        return redirect('reserva')

    hoy = timezone.localdate()
    fecha_limite = hoy + timedelta(days=7)
    fecha_reserva_date = fecha_reserva.date()
    if fecha_reserva_date < hoy or fecha_reserva_date > fecha_limite:
        messages.error(request, 'La fecha debe ser entre hoy y los próximos 7 días.')
        return redirect('reserva')

    ocupadas = _mesa_ids_ocupadas_para_slot(fecha_reserva, hora)
    mesa = (
        MesaModel.objects.filter(capacidad__gte=personas)
        .exclude(id_mesa__in=ocupadas)
        .order_by('numero_mesa')
        .first()
    )
    if not mesa:
        messages.error(
            request,
            'No hay mesas disponibles para esa fecha, hora y número de personas. Prueba otro horario.',
        )
        return redirect('reserva')

    user_autenticado = request.user if request.user.is_authenticated else None

    codigo = f'RES-{uuid.uuid4().hex[:8].upper()}'
    for _ in range(5):
        try:
            ReservaModel.objects.create(
                codigo_reserva=codigo,
                user=user_autenticado,
                nombre_cliente=nombre,
                email_cliente=email,
                telefono_cliente=telefono,
                mesa=mesa,
                fecha_reserva=fecha_reserva,
                hora=hora,
                numero_personas=personas,
                estado='PENDIENTE',
                comentarios=comentarios,
            )
            return redirect(f"{reverse('reserva_confirmada')}?codigo={codigo}")
        except IntegrityError:
            codigo = f'RES-{uuid.uuid4().hex[:8].upper()}'
    messages.error(request, 'No se pudo registrar la reserva. Intenta de nuevo.')
    return redirect('reserva')


def _carrito_items(request):
    return request.session.get(SESSION_CARRITO_KEY, [])


def _carrito_guardar(request, items):
    request.session[SESSION_CARRITO_KEY] = items
    request.session.modified = True


def carrito_view(request):
    items = _carrito_items(request)
    total = sum(float(i['precio']) * int(i['cantidad']) for i in items)
    user = request.user
    rol = _rol_upper_public(user) if user.is_authenticated else ''
    return render(
        request,
        'public/carrito.html',
        {
            'items': items,
            'total': total,
            'puede_finalizar': bool(items) and user.is_authenticated and rol == 'CLIENTE',
            'requiere_login_para_comprar': bool(items) and not user.is_authenticated,
            'rol_no_cliente': bool(items) and user.is_authenticated and rol != 'CLIENTE',
        },
    )


@login_required(login_url='/login/')
@require_POST
def carrito_checkout_view(request):
    if _rol_upper_public(request.user) != 'CLIENTE':
        messages.warning(
            request,
            'Solo las cuentas de cliente pueden finalizar compras desde el sitio web.',
        )
        return redirect('carrito')

    items = _carrito_items(request)
    if not items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    comentarios = (request.POST.get('comentarios') or '').strip() or None
    if comentarios and len(comentarios) > 500:
        comentarios = comentarios[:500]

    lineas = []
    for raw in items:
        try:
            pid = int(raw['producto_id'])
            qty = int(raw['cantidad'])
        except (TypeError, ValueError, KeyError):
            messages.error(request, 'Datos del carrito no válidos.')
            return redirect('carrito')
        if qty < 1:
            continue
        producto = ProductoModel.objects.filter(pk=pid).first()
        if not producto:
            messages.error(
                request,
                f'El producto «{raw.get("nombre", "desconocido")}» ya no está disponible. Actualiza el carrito.',
            )
            return redirect('carrito')
        precio = float(producto.precio)
        lineas.append(
            {
                'producto': producto,
                'cantidad': qty,
                'precio': precio,
                'subtotal': precio * qty,
            }
        )

    if not lineas:
        messages.error(request, 'No quedaron productos válidos en el carrito.')
        return redirect('carrito')

    total = sum(l['subtotal'] for l in lineas)
    user = request.user
    nombre = f'{user.nombre} {user.apellido}'.strip() or user.email

    try:
        with transaction.atomic():
            pedido = PedidoModel.objects.create(
                user=user,
                cliente_nombre=nombre,
                total=total,
                estado='PENDIENTE',
                comentarios=comentarios,
            )
            for ln in lineas:
                DetallePedidoModel.objects.create(
                    pedido=pedido,
                    producto=ln['producto'],
                    cantidad=ln['cantidad'],
                    precio=ln['precio'],
                )
            PagoModel.objects.create(
                pedido=pedido,
                user=user,
                metodo_pago='WEB_PENDIENTE',
                monto_total=total,
                estado='PENDIENTE',
            )

            # Asignación automática del mesero para que el dashboard del empleado funcione.
            mesero = _obtener_mesero_para_asignar()
            if mesero:
                pedido.empleado_asignado = mesero
                pedido.save(update_fields=['empleado_asignado'])
    except Exception:
        messages.error(
            request,
            'No se pudo registrar el pedido. Intenta de nuevo en unos minutos.',
        )
        return redirect('carrito')

    _carrito_guardar(request, [])
    messages.success(
        request,
        f'¡Pedido #{pedido.pk} registrado! Te contactaremos o podrás pagar al recoger.',
    )
    return redirect('pedido_confirmado_publico', pk=pedido.pk)


@login_required(login_url='/login/')
@require_GET
def pedido_confirmado_publico_view(request, pk):
    # Solo cuentas de cliente deben poder ver su pedido confirmado.
    if _rol_upper_public(request.user) != 'CLIENTE':
        messages.warning(request, 'No tienes permiso para ver pedidos confirmados.')
        return redirect('index')

    # Validación básica del parámetro URL.
    try:
        pk_int = int(pk)
    except (TypeError, ValueError):
        messages.warning(request, 'Número de pedido inválido.')
        return redirect('mi_perfil')

    if pk_int < 1:
        messages.warning(request, 'Número de pedido inválido.')
        return redirect('mi_perfil')

    pedido = (
        PedidoModel.objects.select_related('user', 'empleado_asignado')
        .prefetch_related('detalles__producto')
        .filter(pk=pk_int, user=request.user)
        .first()
    )
    if not pedido:
        # Si existe el pedido pero no pertenece al usuario, mostramos un mensaje más claro.
        pedido_existe = PedidoModel.objects.filter(pk=pk_int).only('id').exists()
        if pedido_existe:
            messages.warning(request, 'Ese pedido no pertenece a tu cuenta.')
        else:
            messages.warning(
                request,
                'No encontramos ese pedido. Revisa el numero de pedido o crea uno nuevo.',
            )
        return redirect('mi_perfil')

    # Validación extra: el template asume que existen detalles (items).
    if not pedido.detalles.exists():
        messages.warning(
            request,
            'Este pedido no tiene productos asociados para mostrarlo.',
        )
        return redirect('mi_perfil')
    return render(
        request,
        'public/pedido_confirmado.html',
        {'pedido': pedido},
    )


@require_POST
def carrito_agregar_view(request):
    raw_id = (request.POST.get('producto_id') or '').strip()
    try:
        cantidad = int((request.POST.get('cantidad') or '1').strip() or 1)
    except ValueError:
        cantidad = 1
    if cantidad < 1:
        cantidad = 1
    if cantidad > 99:
        cantidad = 99

    try:
        pid = int(raw_id)
    except ValueError:
        messages.error(request, 'Producto no válido.')
        return redirect('menu')

    try:
        producto = ProductoModel.objects.select_related('categoria').get(pk=pid)
    except ProductoModel.DoesNotExist:
        messages.error(request, 'Ese producto ya no está disponible.')
        return redirect('menu')

    items = list(_carrito_items(request))
    precio = float(producto.precio)
    encontrado = False
    for i in items:
        if int(i['producto_id']) == pid:
            i['cantidad'] = int(i['cantidad']) + cantidad
            i['subtotal'] = precio * i['cantidad']
            encontrado = True
            break
    if not encontrado:
        items.append(
            {
                'producto_id': pid,
                'nombre': producto.nombre,
                'precio': precio,
                'cantidad': cantidad,
                'subtotal': precio * cantidad,
            }
        )

    _carrito_guardar(request, items)
    messages.success(
        request,
        f'«{producto.nombre}» (${format_money_display(precio)} c/u) se agregó al carrito.',
    )
    destino = (request.POST.get('next') or '').strip()
    if destino and url_has_allowed_host_and_scheme(
        destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(destino)
    return redirect('carrito')


@require_POST
def carrito_quitar_view(request):
    raw_id = (request.POST.get('producto_id') or '').strip()
    try:
        pid = int(raw_id)
    except ValueError:
        return redirect('carrito')

    items = [i for i in _carrito_items(request) if int(i['producto_id']) != pid]
    _carrito_guardar(request, items)
    messages.info(request, 'Producto quitado del carrito.')
    return redirect('carrito')


@require_POST
def carrito_vaciar_view(request):
    _carrito_guardar(request, [])
    messages.info(request, 'Carrito vaciado.')
    return redirect('carrito')
