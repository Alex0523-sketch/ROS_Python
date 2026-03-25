"""Reportes administrativos: filtros y exportación PDF."""

from __future__ import annotations

from datetime import date, timedelta
from io import BytesIO

from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from users.infrastructure.models import (
    CategoriaModel,
    HorarioModel,
    InventarioModel,
    MesaModel,
    NoticiaModel,
    PagoModel,
    PedidoModel,
    ProductoModel,
    PromocionModel,
    ReservaModel,
    RolModel,
    UserModel,
)
from users.infrastructure.views.admin_list_views import admin_only


def _parse_date_param(raw: str | None, default: date) -> date:
    if not raw or not str(raw).strip():
        return default
    try:
        return date.fromisoformat(str(raw).strip()[:10])
    except ValueError:
        return default


def _get_filters(request):
    today = timezone.localdate()
    default_start = today - timedelta(days=30)
    fecha_desde = _parse_date_param(request.GET.get('fecha_desde'), default_start)
    fecha_hasta = _parse_date_param(request.GET.get('fecha_hasta'), today)
    if fecha_desde > fecha_hasta:
        fecha_desde, fecha_hasta = fecha_hasta, fecha_desde

    estado_pedido = (request.GET.get('estado_pedido') or '').strip()
    estado_pago = (request.GET.get('estado_pago') or '').strip()
    estado_reserva = (request.GET.get('estado_reserva') or '').strip()
    estado_mesa = (request.GET.get('estado_mesa') or '').strip()
    buscar = (request.GET.get('buscar') or '').strip()
    categoria_id = (request.GET.get('categoria_id') or '').strip()
    rol_id = (request.GET.get('rol_id') or '').strip()
    mesas_modo = (request.GET.get('mesas_modo') or 'todas').strip()
    if mesas_modo not in ('todas', 'creadas'):
        mesas_modo = 'todas'

    def _chk(name: str, default: bool = True) -> bool:
        if request.GET.get('aplicar') != '1':
            return default
        return request.GET.get(name) == '1'

    secciones = {
        'pedidos': _chk('incl_pedidos'),
        'pagos': _chk('incl_pagos'),
        'reservas': _chk('incl_reservas'),
        'mesas': _chk('incl_mesas'),
        'usuarios': _chk('incl_usuarios'),
        'productos': _chk('incl_productos'),
        'noticias': _chk('incl_noticias'),
        'horarios': _chk('incl_horarios'),
        'inventario': _chk('incl_inventario'),
        'promociones': _chk('incl_promociones'),
    }

    return {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado_pedido': estado_pedido,
        'estado_pago': estado_pago,
        'estado_reserva': estado_reserva,
        'estado_mesa': estado_mesa,
        'buscar': buscar,
        'categoria_id': categoria_id,
        'rol_id': rol_id,
        'mesas_modo': mesas_modo,
        'secciones': secciones,
    }


def _build_report_data(f: dict):
    desde, hasta = f['fecha_desde'], f['fecha_hasta']
    buscar = f['buscar']

    pedidos = PedidoModel.objects.select_related('user', 'empleado_asignado').order_by('-fecha_creacion')
    pedidos = pedidos.filter(fecha_creacion__date__gte=desde, fecha_creacion__date__lte=hasta)
    if f['estado_pedido']:
        pedidos = pedidos.filter(estado=f['estado_pedido'])
    if buscar:
        pedidos = pedidos.filter(
            Q(cliente_nombre__icontains=buscar)
            | Q(numero_mesa__icontains=buscar)
            | Q(comentarios__icontains=buscar)
        )

    pagos = PagoModel.objects.select_related('user', 'pedido').order_by('-fecha_creacion')
    pagos = pagos.filter(fecha_creacion__date__gte=desde, fecha_creacion__date__lte=hasta)
    if f['estado_pago']:
        pagos = pagos.filter(estado=f['estado_pago'])

    reservas = ReservaModel.objects.select_related('mesa', 'user').order_by('-fecha_reserva')
    reservas = reservas.filter(fecha_reserva__date__gte=desde, fecha_reserva__date__lte=hasta)
    if f['estado_reserva']:
        reservas = reservas.filter(estado=f['estado_reserva'])
    if buscar:
        reservas = reservas.filter(
            Q(nombre_cliente__icontains=buscar)
            | Q(codigo_reserva__icontains=buscar)
            | Q(email_cliente__icontains=buscar)
            | Q(telefono_cliente__icontains=buscar)
        )

    mesas = MesaModel.objects.all().order_by('numero_mesa')
    if f['estado_mesa']:
        mesas = mesas.filter(estado=f['estado_mesa'])
    if f['mesas_modo'] == 'creadas':
        mesas = mesas.filter(fecha_creacion__date__gte=desde, fecha_creacion__date__lte=hasta)

    usuarios = UserModel.objects.select_related('rol').order_by('nombre', 'apellido')
    usuarios = usuarios.filter(fecha_creacion__date__gte=desde, fecha_creacion__date__lte=hasta)
    if f['rol_id']:
        try:
            usuarios = usuarios.filter(rol_id=int(f['rol_id']))
        except ValueError:
            pass
    if buscar:
        usuarios = usuarios.filter(
            Q(nombre__icontains=buscar) | Q(apellido__icontains=buscar) | Q(email__icontains=buscar)
        )

    productos = ProductoModel.objects.select_related('categoria').order_by('nombre')
    productos = productos.filter(created_at__date__gte=desde, created_at__date__lte=hasta)
    if f['categoria_id']:
        try:
            productos = productos.filter(categoria_id=int(f['categoria_id']))
        except ValueError:
            pass
    if buscar:
        productos = productos.filter(Q(nombre__icontains=buscar) | Q(descripcion__icontains=buscar))

    noticias = NoticiaModel.objects.all().order_by('-fecha_publicacion', '-id')
    noticias = noticias.filter(
        Q(
            fecha_publicacion__isnull=False,
            fecha_publicacion__gte=desde,
            fecha_publicacion__lte=hasta,
        )
        | Q(
            fecha_publicacion__isnull=True,
            fecha_actualizacion__date__gte=desde,
            fecha_actualizacion__date__lte=hasta,
        )
    )
    if buscar:
        noticias = noticias.filter(Q(titulo__icontains=buscar) | Q(contenido__icontains=buscar))

    horarios = HorarioModel.objects.select_related('user').order_by('user__nombre', 'dia_semana')
    horarios = horarios.filter(fecha_creacion__date__gte=desde, fecha_creacion__date__lte=hasta)
    if buscar:
        horarios = horarios.filter(
            Q(user__nombre__icontains=buscar)
            | Q(user__apellido__icontains=buscar)
            | Q(dia_semana__icontains=buscar)
        )

    inventario = InventarioModel.objects.select_related('producto').order_by('producto__nombre')
    inventario = inventario.filter(fecha_creacion__date__gte=desde, fecha_creacion__date__lte=hasta)
    if buscar:
        inventario = inventario.filter(producto__nombre__icontains=buscar)

    promociones = PromocionModel.objects.prefetch_related('productos').order_by('-fecha_inicio')
    promociones = promociones.filter(
        Q(fecha_inicio__lte=hasta, fecha_fin__gte=desde)
        | Q(created_at__date__gte=desde, created_at__date__lte=hasta)
    )
    if buscar:
        promociones = promociones.filter(Q(titulo__icontains=buscar) | Q(descripcion__icontains=buscar))

    total_pedidos_monto = pedidos.aggregate(s=Sum('total'))['s'] or 0
    total_pagos_monto = pagos.aggregate(s=Sum('monto_total'))['s'] or 0

    return {
        'filters': f,
        'pedidos': list(pedidos[:500]),
        'pedidos_count': pedidos.count(),
        'pagos': list(pagos[:500]),
        'pagos_count': pagos.count(),
        'reservas': list(reservas[:500]),
        'reservas_count': reservas.count(),
        'mesas': list(mesas[:500]),
        'mesas_count': mesas.count(),
        'usuarios': list(usuarios[:500]),
        'usuarios_count': usuarios.count(),
        'productos': list(productos[:500]),
        'productos_count': productos.count(),
        'noticias': list(noticias[:200]),
        'noticias_count': noticias.count(),
        'horarios': list(horarios[:500]),
        'horarios_count': horarios.count(),
        'inventario': list(inventario[:500]),
        'inventario_count': inventario.count(),
        'promociones': list(promociones[:200]),
        'promociones_count': promociones.count(),
        'total_pedidos_monto': float(total_pedidos_monto),
        'total_pagos_monto': float(total_pagos_monto),
    }


def _pdf_cell(text: str, max_len: int = 80) -> str:
    t = (text or '').replace('\n', ' ').replace('\r', '')
    if len(t) > max_len:
        return t[: max_len - 1] + '…'
    return t


def _build_pdf(report: dict) -> bytes:
    f = report['filters']
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title='Reporte Olla y Sazón',
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'T',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#1a1a1a'),
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=11,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.HexColor('#333333'),
    )
    small = ParagraphStyle('S', parent=styles['Normal'], fontSize=8, leading=10)

    story = []
    story.append(Paragraph('Olla y Sazón — Reporte consolidado', title_style))
    story.append(
        Paragraph(
            f'<b>Periodo:</b> {f["fecha_desde"].strftime("%d/%m/%Y")} al {f["fecha_hasta"].strftime("%d/%m/%Y")} &nbsp;·&nbsp; '
            f'<b>Generado:</b> {timezone.now().strftime("%d/%m/%Y %H:%M")}',
            styles['Normal'],
        )
    )
    story.append(Spacer(1, 0.3 * cm))

    filtros_txt = []
    if f['estado_pedido']:
        filtros_txt.append(f'Pedido estado: {f["estado_pedido"]}')
    if f['estado_pago']:
        filtros_txt.append(f'Pago estado: {f["estado_pago"]}')
    if f['estado_reserva']:
        filtros_txt.append(f'Reserva estado: {f["estado_reserva"]}')
    if f['estado_mesa']:
        filtros_txt.append(f'Mesa estado: {f["estado_mesa"]}')
    if f['buscar']:
        filtros_txt.append(f'Búsqueda: {f["buscar"]}')
    if f.get('mesas_modo') == 'creadas':
        filtros_txt.append('Mesas: solo creadas en periodo')
    if filtros_txt:
        story.append(Paragraph('<b>Filtros aplicados:</b> ' + ' · '.join(filtros_txt), styles['Normal']))
        story.append(Spacer(1, 0.2 * cm))

    sec = f['secciones']
    story.append(
        Paragraph(
            f'<b>Resumen:</b> Pedidos S/ {report["total_pedidos_monto"]:.2f} &nbsp;|&nbsp; '
            f'Pagos registrados S/ {report["total_pagos_monto"]:.2f}',
            styles['Normal'],
        )
    )
    story.append(Spacer(1, 0.4 * cm))

    def add_table(title: str, headers: list[str], rows: list[list], note_count: int | None = None):
        story.append(Paragraph(title, h2_style))
        if note_count is not None and note_count > len(rows):
            story.append(Paragraph(f'<i>Mostrando {len(rows)} de {note_count} registros.</i>', small))
        data = [headers] + rows
        if len(data) == 1:
            data.append(['Sin registros en este periodo / filtros.'])
        t = Table(data, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffd700')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f8f8')]),
                ]
            )
        )
        story.append(t)
        story.append(Spacer(1, 0.25 * cm))

    if sec['pedidos']:
        rows = []
        for p in report['pedidos']:
            rows.append(
                [
                    str(p.id),
                    _pdf_cell(p.cliente_nombre),
                    _pdf_cell(p.estado, 20),
                    f'{p.total:.2f}',
                    p.fecha_creacion.strftime('%d/%m/%Y %H:%M') if p.fecha_creacion else '',
                ]
            )
        add_table(
            'Pedidos',
            ['ID', 'Cliente', 'Estado', 'Total S/', 'Fecha'],
            rows,
            report['pedidos_count'],
        )

    if sec['pagos']:
        rows = []
        for p in report['pagos']:
            rows.append(
                [
                    str(p.id),
                    str(p.pedido_id),
                    _pdf_cell(p.metodo_pago, 15),
                    f'{p.monto_total:.2f}',
                    _pdf_cell(p.estado, 15),
                    p.fecha_creacion.strftime('%d/%m/%Y') if p.fecha_creacion else '',
                ]
            )
        add_table(
            'Pagos',
            ['ID', 'Pedido', 'Método', 'Monto S/', 'Estado', 'Fecha'],
            rows,
            report['pagos_count'],
        )

    if sec['reservas']:
        rows = []
        for r in report['reservas']:
            if r.user_id and getattr(r, 'user', None) is not None:
                cli = f'{r.user.nombre} {r.user.apellido}'
            else:
                cli = r.nombre_cliente or ''
            rows.append(
                [
                    _pdf_cell(r.codigo_reserva or '—', 14),
                    _pdf_cell(cli, 28),
                    str(r.mesa_id) if r.mesa_id else '',
                    str(r.numero_personas),
                    _pdf_cell(r.estado, 14),
                    r.fecha_reserva.strftime('%d/%m/%Y %H:%M') if r.fecha_reserva else '',
                ]
            )
        add_table(
            'Reservas',
            ['Código', 'Cliente', 'Mesa', 'Pers.', 'Estado', 'Fecha'],
            rows,
            report['reservas_count'],
        )

    if sec['mesas']:
        rows = []
        for m in report['mesas']:
            rows.append(
                [
                    str(m.id_mesa),
                    str(m.numero_mesa),
                    str(m.capacidad),
                    _pdf_cell(m.estado, 15),
                    _pdf_cell(m.ubicacion or '', 25),
                ]
            )
        titulo_mesas = 'Mesas (todas; filtro por estado)' if f.get('mesas_modo') != 'creadas' else 'Mesas (creadas en el periodo)'
        add_table(
            titulo_mesas,
            ['ID', 'Nº', 'Cap.', 'Estado', 'Ubicación'],
            rows,
            report['mesas_count'],
        )

    if sec['usuarios']:
        rows = []
        for u in report['usuarios']:
            rol = u.rol.nombre if getattr(u, 'rol_id', None) and u.rol else ''
            rows.append(
                [
                    str(u.id_user),
                    _pdf_cell(f'{u.nombre} {u.apellido}', 35),
                    _pdf_cell(u.email, 40),
                    _pdf_cell(rol, 18),
                    u.fecha_creacion.strftime('%d/%m/%Y') if u.fecha_creacion else '',
                ]
            )
        add_table(
            'Usuarios (altas en periodo)',
            ['ID', 'Nombre', 'Email', 'Rol', 'Alta'],
            rows,
            report['usuarios_count'],
        )

    if sec['productos']:
        rows = []
        for p in report['productos']:
            cat = p.categoria.nombre if p.categoria_id else ''
            rows.append(
                [
                    str(p.id_producto),
                    _pdf_cell(p.nombre, 35),
                    f'{p.precio:.2f}',
                    _pdf_cell(cat, 22),
                    p.created_at.strftime('%d/%m/%Y') if p.created_at else '',
                ]
            )
        add_table(
            'Productos',
            ['ID', 'Nombre', 'Precio', 'Categoría', 'Alta'],
            rows,
            report['productos_count'],
        )

    if sec['noticias']:
        rows = []
        for n in report['noticias']:
            rows.append(
                [
                    str(n.id),
                    _pdf_cell(n.titulo, 55),
                    n.fecha_publicacion.strftime('%d/%m/%Y') if n.fecha_publicacion else '—',
                ]
            )
        add_table(
            'Noticias',
            ['ID', 'Título', 'Publicación'],
            rows,
            report['noticias_count'],
        )

    if sec['horarios']:
        rows = []
        for h in report['horarios']:
            un = f'{h.user.nombre} {h.user.apellido}' if h.user_id else ''
            rows.append(
                [
                    str(h.id),
                    _pdf_cell(un, 35),
                    _pdf_cell(h.dia_semana, 14),
                    h.hora_inicio,
                    h.hora_fin,
                ]
            )
        add_table(
            'Horarios',
            ['ID', 'Empleado', 'Día', 'Inicio', 'Fin'],
            rows,
            report['horarios_count'],
        )

    if sec['inventario']:
        rows = []
        for i in report['inventario']:
            rows.append(
                [
                    str(i.id),
                    _pdf_cell(i.producto.nombre, 45),
                    str(i.cantidad_disponible),
                    str(i.cantidad_minima),
                ]
            )
        add_table(
            'Inventario (movimientos en periodo)',
            ['ID', 'Producto', 'Stock', 'Mín.'],
            rows,
            report['inventario_count'],
        )

    if sec['promociones']:
        rows = []
        for pr in report['promociones']:
            rows.append(
                [
                    str(getattr(pr, 'id_promocion', pr.pk)),
                    _pdf_cell(pr.titulo, 40),
                    f'{pr.descuento:.1f}%',
                    pr.fecha_inicio.strftime('%d/%m/%Y') if pr.fecha_inicio else '',
                    pr.fecha_fin.strftime('%d/%m/%Y') if pr.fecha_fin else '',
                ]
            )
        add_table(
            'Promociones',
            ['ID', 'Título', 'Dto.', 'Inicio', 'Fin'],
            rows,
            report['promociones_count'],
        )

    doc.build(story)
    pdf = buf.getvalue()
    buf.close()
    return pdf


@admin_only
def reportes_admin_view(request):
    f = _get_filters(request)
    report = _build_report_data(f)
    categorias = CategoriaModel.objects.order_by('nombre')
    roles = RolModel.objects.order_by('nombre')
    estados_pedido = (
        PedidoModel.objects.order_by('estado').values_list('estado', flat=True).distinct()
    )
    estados_pago = PagoModel.objects.order_by('estado').values_list('estado', flat=True).distinct()
    estados_reserva = ReservaModel.objects.order_by('estado').values_list('estado', flat=True).distinct()
    estados_mesa = MesaModel.objects.order_by('estado').values_list('estado', flat=True).distinct()

    return render(
        request,
        'admin/reportes_index.html',
        {
            'report': report,
            'f': f,
            'categorias': categorias,
            'roles': roles,
            'estados_pedido': list(estados_pedido),
            'estados_pago': list(estados_pago),
            'estados_reserva': list(estados_reserva),
            'estados_mesa': list(estados_mesa),
        },
    )


@admin_only
def reportes_pdf_view(request):
    f = _get_filters(request)
    report = _build_report_data(f)
    pdf_bytes = _build_pdf(report)
    nombre = f'reporte_olla_sazon_{f["fecha_desde"]}_{f["fecha_hasta"]}.pdf'
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre}"'
    return response
