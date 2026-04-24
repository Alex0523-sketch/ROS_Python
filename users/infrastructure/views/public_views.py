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
        productos_qs = productos_qs.filter(categoria_id=categoria_seleccionada)

    # Determinar qué productos tienen algún insumo bajo el stock mínimo
    from users.infrastructure.models.receta_item_model import RecetaItemModel
    from django.db.models import F
    insumos_sin_stock = set(
        RecetaItemModel.objects
        .filter(insumo__stock_actual__lt=F('insumo__stock_minimo'))
        .values_list('producto_id', flat=True)
    )

    productos = []
    for p in productos_qs:
        p.sin_stock = p.pk in insumos_sin_stock
        productos.append(p)

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
    es_cliente = user.is_authenticated and rol == 'CLIENTE'
    es_invitado = not user.is_authenticated
    return render(
        request,
        'public/carrito.html',
        {
            'items': items,
            'total': total,
            'puede_finalizar': bool(items) and (es_cliente or es_invitado),
            'requiere_login_para_comprar': False,
            'rol_no_cliente': bool(items) and user.is_authenticated and rol not in ('CLIENTE', ''),
            'es_invitado': es_invitado,
        },
    )


@require_POST
def carrito_checkout_view(request):
    user = request.user
    if user.is_authenticated and _rol_upper_public(user) not in ('CLIENTE', ''):
        messages.warning(request, 'Solo las cuentas de cliente pueden finalizar compras desde el sitio web.')
        return redirect('carrito')

    items = _carrito_items(request)
    if not items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    # Resolver identidad
    if user.is_authenticated:
        nombre = f'{user.nombre} {user.apellido}'.strip() or user.email
        user_obj = user
    else:
        nombre = (request.POST.get('nombre_invitado') or '').strip()
        if len(nombre) < 3:
            messages.error(request, 'Ingresa tu nombre para continuar como invitado.')
            return redirect('carrito')
        user_obj = None

    comentarios = (request.POST.get('comentarios') or '').strip() or None
    if comentarios and len(comentarios) > 500:
        comentarios = comentarios[:500]

    lineas = []
    total = 0
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
            messages.error(request, f'El producto «{raw.get("nombre", "desconocido")}» ya no está disponible.')
            return redirect('carrito')
        precio = float(producto.precio)
        subtotal = precio * qty
        total += subtotal
        lineas.append({'producto': producto, 'cantidad': qty, 'precio': precio, 'subtotal': subtotal})

    if not lineas:
        messages.error(request, 'No quedaron productos válidos en el carrito.')
        return redirect('carrito')

    # Registrar el pedido INMEDIATAMENTE en estado PENDIENTE
    try:
        with transaction.atomic():
            pedido = PedidoModel.objects.create(
                user=user_obj,
                cliente_nombre=nombre,
                total=total,
                estado='PENDIENTE',
                comentarios=comentarios,
            )
            for l in lineas:
                DetallePedidoModel.objects.create(
                    pedido=pedido,
                    producto=l['producto'],
                    cantidad=l['cantidad'],
                    precio=l['precio'],
                )
            mesero = _obtener_mesero_para_asignar()
            if mesero:
                pedido.empleado_asignado = mesero
                pedido.save(update_fields=['empleado_asignado'])

            # Descontar stock de insumos según receta de cada producto
            from users.application.use_cases.inventario_usecase import DescontarInventarioPorPedidoUseCase
            DescontarInventarioPorPedidoUseCase().execute(pedido.pk)
    except Exception:
        messages.error(request, 'No se pudo registrar el pedido. Intenta de nuevo.')
        return redirect('carrito')

    _carrito_guardar(request, [])
    request.session['pedido_id'] = pedido.pk
    request.session.modified = True

    return redirect('pedido_confirmado_publico', pk=pedido.pk)


@require_POST
def pedido_procesar_pago_view(request):
    user = request.user
    if user.is_authenticated and _rol_upper_public(user) not in ('CLIENTE', ''):
        return redirect('carrito')

    pedido_id = request.session.get('pedido_id')
    if not pedido_id:
        messages.error(request, 'Sesión expirada. Vuelve a intentarlo.')
        return redirect('carrito')

    pedido = PedidoModel.objects.filter(pk=pedido_id).first()
    if not pedido:
        messages.error(request, 'No se encontró el pedido.')
        return redirect('carrito')

    METODOS_VALIDOS = {'EFECTIVO', 'DATAFONO', 'TARJETA_VIRTUAL', 'NEQUI', 'DAVIPLATA'}
    metodo = (request.POST.get('metodo_pago') or '').strip().upper()
    if metodo not in METODOS_VALIDOS:
        messages.error(request, 'Selecciona un método de pago válido.')
        return redirect('pedido_confirmado_publico', pk=pedido_id)

    DIGITALES = {'TARJETA_VIRTUAL', 'NEQUI', 'DAVIPLATA'}
    estado_pago = 'PAGADO' if metodo in DIGITALES else 'PENDIENTE'
    estado_pedido = 'CONFIRMADO' if metodo in DIGITALES else 'PENDIENTE'

    user_obj = user if user.is_authenticated else None

    try:
        with transaction.atomic():
            PagoModel.objects.create(
                pedido=pedido,
                user=user_obj,
                metodo_pago=metodo,
                monto_total=pedido.total,
                estado=estado_pago,
            )
            pedido.estado = estado_pedido
            pedido.save(update_fields=['estado'])
    except Exception:
        messages.error(request, 'No se pudo registrar el pago. Intenta de nuevo.')
        return redirect('pedido_confirmado_publico', pk=pedido_id)

    request.session.pop('pedido_id', None)
    request.session.modified = True

    return redirect('pedido_confirmado_publico', pk=pedido.pk)


@require_GET
def pedido_confirmado_publico_view(request, pk):
    try:
        pk_int = int(pk)
        assert pk_int > 0
    except (TypeError, ValueError, AssertionError):
        messages.warning(request, 'Número de pedido inválido.')
        return redirect('index')

    # Verificar que el pedido pertenece a quien lo hizo (usuario o sesión invitado)
    qs = PedidoModel.objects.select_related('user', 'empleado_asignado').prefetch_related('detalles__producto')
    pedido = qs.filter(pk=pk_int).first()

    if not pedido:
        messages.warning(request, 'No encontramos ese pedido.')
        return redirect('index')

    user = request.user
    if user.is_authenticated:
        if pedido.user_id and pedido.user_id != user.pk:
            messages.warning(request, 'Ese pedido no pertenece a tu cuenta.')
            return redirect('mi_perfil')
    # Para invitados no hay verificación adicional (el pk viene de la redirección inmediata)

    if not pedido.detalles.exists():
        messages.warning(request, 'Este pedido no tiene productos asociados.')
        return redirect('index')

    return render(request, 'public/pedido_confirmado.html', {'pedido': pedido})


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
