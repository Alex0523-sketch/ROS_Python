from __future__ import annotations

from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render
from django.utils import timezone

from users.application.application.use_cases.pedido_usecase import CambiarEstadoPedidoUseCase
from users.infrastructure.models import (
    DetallePedidoModel,
    MesaModel,
    NoticiaModel,
    PagoModel,
    PedidoModel,
    ProductoModel,
    ReservaModel,
    UserModel,
)
from users.infrastructure.models.horario_model import HorarioModel
from users.infrastructure.repositories.pedido_repository_impl import PedidoRepositoryImpl


def _rol_upper(user):
    r = getattr(user, 'rol', None)
    raw = (r.nombre or '').strip().upper() if r else ''
    if raw in ('ADMIN', 'ADMINISTRADOR'):
        return 'ADMINISTRADOR'
    return raw


def _coerce_orm_day(val):
    """Unifica valores de TruncDate (date/datetime/str según motor) a `date` para alinear con el eje X."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return timezone.localtime(val).date() if timezone.is_aware(val) else val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        return date.fromisoformat(val.strip()[:10])
    return val


def _pedidos_cliente_qs(user):
    """Pedidos del usuario excluyendo cancelados (comparación insensible a mayúsculas)."""
    return PedidoModel.objects.filter(user=user).exclude(
        Q(estado__iexact='CANCELADO') | Q(estado__iexact='CANCELADA')
    )


@login_required(login_url='/login/')
def mi_perfil_view(request):
    if _rol_upper(request.user) != 'CLIENTE':
        messages.warning(request, 'No tienes permiso para acceder a esa sección.')
        return redirect('index')

    user = request.user
    pedidos_qs = _pedidos_cliente_qs(user)
    total_gastado = float(pedidos_qs.aggregate(s=Sum('total')).get('s') or 0.0)
    pedidos_count = pedidos_qs.count()

    fav = (
        DetallePedidoModel.objects.filter(pedido__in=pedidos_qs)
        .values('producto_id', 'producto__nombre')
        .annotate(total_qty=Sum('cantidad'))
        .order_by('-total_qty')
        .first()
    )
    plato_favorito = None
    favorito_cantidad = 0
    if fav:
        plato_favorito = fav.get('producto__nombre')
        favorito_cantidad = int(fav.get('total_qty') or 0)

    ultimos_pedidos = list(
        pedidos_qs.select_related('empleado_asignado').order_by('-fecha_creacion')[:8]
    )

    reservas_qs = ReservaModel.objects.filter(user=user).order_by('-fecha_reserva')
    reservas_count = reservas_qs.count()
    ultimas_reservas = list(reservas_qs[:5])

    return render(
        request,
        'cliente/perfil_panel.html',
        {
            'total_gastado': total_gastado,
            'pedidos_count': pedidos_count,
            'plato_favorito': plato_favorito,
            'favorito_cantidad': favorito_cantidad,
            'ultimos_pedidos': ultimos_pedidos,
            'reservas_count': reservas_count,
            'ultimas_reservas': ultimas_reservas,
        },
    )


@login_required(login_url='/login/')
def mi_horario_view(request):
    if _rol_upper(request.user) != 'EMPLEADO':
        messages.warning(request, 'No tienes permiso para acceder a esa sección.')
        return redirect('index')
    qs = HorarioModel.objects.filter(user=request.user).select_related('user')

    horarios = list(qs)
    day_order = {
        'LUNES': 0,
        'MARTES': 1,
        'MIERCOLES': 2,
        'MIÉRCOLES': 2,
        'JUEVES': 3,
        'VIERNES': 4,
        'SABADO': 5,
        'SÁBADO': 5,
        'DOMINGO': 6,
    }

    def _sort_key(h):
        dia = (h.dia_semana or '').strip().upper()
        return (day_order.get(dia, 99), h.hora_inicio or '', h.hora_fin or '')

    horarios.sort(key=_sort_key)

    # Agrupamos por día para mostrarlo más claro en la UI.
    dias_horarios = []
    seen = set()
    for h in horarios:
        dia = (h.dia_semana or '').strip()
        if dia not in seen:
            seen.add(dia)
            dias_horarios.append({'dia': dia, 'intervalos': []})
        dias_horarios[-1]['intervalos'].append(h)

    total_turnos = len(horarios)
    dias_count = len(dias_horarios)
    proxima_entrada = min((h.hora_inicio for h in horarios if h.hora_inicio), default=None)

    return render(
        request,
        'empleado/mi_horario_panel.html',
        {
            'horarios': horarios,
            'dias_horarios': dias_horarios,
            'total_turnos': total_turnos,
            'dias_count': dias_count,
            'proxima_entrada': proxima_entrada,
        },
    )


@login_required(login_url='/login/')
def pedidos_asignados_view(request):
    if _rol_upper(request.user) != 'EMPLEADO':
        messages.warning(request, 'No tienes permiso para acceder a esa sección.')
        return redirect('index')

    repo = PedidoRepositoryImpl()
    qs = (
        PedidoModel.objects.select_related('user', 'empleado_asignado')
        .prefetch_related('detalles__producto')
        .filter(empleado_asignado=request.user)
        .order_by('-fecha_creacion')
    )

    estados = ['PENDIENTE', 'EN_PREPARACION', 'LISTO', 'ENTREGADO', 'CANCELADO']
    pedidos_counts = {e: qs.filter(estado=e).count() for e in estados}

    # Transiciones permitidas para empleados.
    transiciones = {
        'PENDIENTE': ['EN_PREPARACION', 'CANCELADO'],
        'EN_PREPARACION': ['LISTO', 'CANCELADO'],
        'LISTO': ['ENTREGADO', 'CANCELADO'],
        'ENTREGADO': [],
        'CANCELADO': [],
    }

    pedidos = list(qs)
    for p in pedidos:
        p.allowed_next = transiciones.get(getattr(p, 'estado', None), [])

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        nuevo_estado = (request.POST.get('nuevo_estado') or '').strip().upper()
        if not pedido_id or not nuevo_estado:
            messages.error(request, 'Datos del formulario inválidos.')
            return redirect('pedidos_asignados')

        try:
            pedido_id_int = int(pedido_id)
        except ValueError:
            messages.error(request, 'ID de pedido inválido.')
            return redirect('pedidos_asignados')

        pedido = (
            PedidoModel.objects.filter(pk=pedido_id_int, empleado_asignado=request.user)
            .select_related('user')
            .first()
        )
        if not pedido:
            messages.error(request, 'Ese pedido no te pertenece.')
            return redirect('pedidos_asignados')

        allowed = transiciones.get(pedido.estado, [])
        if nuevo_estado not in allowed:
            messages.error(request, 'No puedes cambiar el pedido a ese estado desde su estado actual.')
            return redirect('pedidos_asignados')

        try:
            CambiarEstadoPedidoUseCase(repo).execute(pedido_id_int, nuevo_estado)
            messages.success(request, f'Pedido actualizado a «{nuevo_estado}».')
        except Exception as exc:
            messages.error(request, f'No se pudo actualizar el pedido: {exc}')

        return redirect('pedidos_asignados')

    return render(
        request,
        'empleado/pedidos_asignados_panel.html',
        {
            'pedidos': pedidos,
            'pedidos_counts': pedidos_counts,
            'transiciones': transiciones,
        },
    )


@login_required(login_url='/login/')
def admin_dashboard_view(request):
    if _rol_upper(request.user) != 'ADMINISTRADOR':
        messages.warning(request, 'No tienes permiso para acceder a esa sección.')
        return redirect('index')

    today = timezone.localdate()
    start = today - timedelta(days=6)
    tz = timezone.get_current_timezone()

    pedidos_by_day = {}
    for row in (
        PedidoModel.objects.filter(fecha_creacion__date__gte=start)
        .annotate(day=TruncDate("fecha_creacion", tzinfo=tz))
        .values("day")
        .annotate(c=Count("id"))
        .order_by("day")
    ):
        d = _coerce_orm_day(row["day"])
        if d is not None:
            pedidos_by_day[d] = row["c"]

    reservas_by_day = {}
    for row in (
        ReservaModel.objects.filter(fecha_creacion__date__gte=start)
        .annotate(day=TruncDate("fecha_creacion", tzinfo=tz))
        .values("day")
        .annotate(c=Count("id"))
        .order_by("day")
    ):
        d = _coerce_orm_day(row["day"])
        if d is not None:
            reservas_by_day[d] = row["c"]

    ingresos_by_day = {}
    for row in (
        PagoModel.objects.filter(fecha_creacion__date__gte=start)
        .annotate(day=TruncDate("fecha_creacion", tzinfo=tz))
        .values("day")
        .annotate(s=Sum("monto_total"))
        .order_by("day")
    ):
        d = _coerce_orm_day(row["day"])
        if d is not None:
            ingresos_by_day[d] = float(row["s"] or 0.0)

    labels = [(start + timedelta(days=i)) for i in range(7)]
    chart_labels = [d.strftime("%d/%m") for d in labels]
    chart_pedidos = [int(pedidos_by_day.get(d, 0)) for d in labels]
    chart_reservas = [int(reservas_by_day.get(d, 0)) for d in labels]
    chart_ingresos = [float(ingresos_by_day.get(d, 0.0)) for d in labels]

    ingresos_total = float(PagoModel.objects.aggregate(s=Sum("monto_total")).get("s") or 0.0)
    ingresos_mes = float(
        PagoModel.objects.filter(
            fecha_creacion__year=today.year,
            fecha_creacion__month=today.month,
        ).aggregate(s=Sum("monto_total")).get("s")
        or 0.0
    )
    ingresos_hoy = float(
        PagoModel.objects.filter(fecha_creacion__date=today).aggregate(s=Sum("monto_total")).get("s")
        or 0.0
    )

    pedidos_hoy = PedidoModel.objects.filter(fecha_creacion__date=today).count()
    reservas_hoy = ReservaModel.objects.filter(fecha_creacion__date=today).count()
    pedidos_pendientes = PedidoModel.objects.filter(estado="PENDIENTE").count()
    pagos_pendientes = PagoModel.objects.filter(estado="PENDIENTE").count()
    mesas_total = MesaModel.objects.count()
    mesas_libres = MesaModel.objects.filter(estado="libre").count()
    empleados_count = UserModel.objects.filter(
        activo=True, rol__nombre__iexact="EMPLEADO"
    ).count()
    empleados_preview = list(
        UserModel.objects.filter(activo=True, rol__nombre__iexact="EMPLEADO")
        .select_related("rol")
        .order_by("nombre", "apellido")[:10]
    )

    kpi = {
        "usuarios": UserModel.objects.count(),
        "empleados": empleados_count,
        "productos": ProductoModel.objects.count(),
        "noticias": NoticiaModel.objects.count(),
        "pedidos": PedidoModel.objects.count(),
        "reservas": ReservaModel.objects.count(),
        "ingresos_total": ingresos_total,
        "ingresos_mes": ingresos_mes,
        "ingresos_hoy": ingresos_hoy,
        "pedidos_hoy": pedidos_hoy,
        "reservas_hoy": reservas_hoy,
        "pedidos_pendientes": pedidos_pendientes,
        "pagos_pendientes": pagos_pendientes,
        "mesas_total": mesas_total,
        "mesas_libres": mesas_libres,
    }

    chart_data = {
        "labels": chart_labels,
        "pedidos": chart_pedidos,
        "reservas": chart_reservas,
        "ingresos": chart_ingresos,
    }

    ultimos_pedidos = list(
        PedidoModel.objects.select_related("user", "empleado_asignado")
        .order_by("-fecha_creacion")[:5]
    )
    ultimas_reservas = list(
        ReservaModel.objects.select_related("mesa", "user")
        .order_by("-fecha_creacion")[:5]
    )

    return render(
        request,
        "admin/dashboard.html",
        {
            "kpi": kpi,
            "ultimos_pedidos": ultimos_pedidos,
            "ultimas_reservas": ultimas_reservas,
            "empleados_preview": empleados_preview,
            "chart_data": chart_data,
            "hoy_label": today.strftime("%d/%m/%Y"),
        },
    )
