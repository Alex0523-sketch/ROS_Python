from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from users.application.use_cases.inventario_usecase import ReporteReposicionUseCase
from users.infrastructure.models.insumo_model import InsumoModel
from users.infrastructure.models.producto_model import ProductoModel
from users.infrastructure.models.receta_item_model import RecetaItemModel
from users.infrastructure.views.panel_views import _rol_upper


def admin_only(view_func):
    @wraps(view_func)
    @login_required(login_url='/login/')
    def _wrapped(request, *args, **kwargs):
        if _rol_upper(request.user) != 'ADMINISTRADOR':
            messages.warning(request, 'No tienes permiso para acceder a esa sección.')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped


@admin_only
def insumos_list_view(request):
    qs = InsumoModel.objects.all().order_by('nombre')
    q_nombre = (request.GET.get('nombre') or '').strip()
    q_unidad = (request.GET.get('unidad') or '').strip()
    q_estado = (request.GET.get('estado') or '').strip()
    if q_nombre:
        qs = qs.filter(nombre__icontains=q_nombre)
    if q_unidad:
        qs = qs.filter(unidad=q_unidad)
    if q_estado == 'reponer':
        from django.db.models import F
        qs = qs.filter(stock_actual__lte=F('stock_minimo'))
    elif q_estado == 'ok':
        from django.db.models import F
        qs = qs.filter(stock_actual__gt=F('stock_minimo'))
    return render(request, 'admin/insumos_list.html', {
        'insumos': qs,
        'q_nombre': q_nombre,
        'q_unidad': q_unidad,
        'q_estado': q_estado,
    })


@admin_only
def insumo_create_view(request):
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        unidad = (request.POST.get('unidad') or 'g').strip()
        try:
            stock_actual = float((request.POST.get('stock_actual') or '0').replace(',', '.'))
            stock_minimo = float((request.POST.get('stock_minimo') or '0').replace(',', '.'))
        except ValueError:
            messages.error(request, 'Los valores de stock deben ser números.')
            return render(request, 'admin/insumo_form.html', {'posted': request.POST}, status=400)

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return render(request, 'admin/insumo_form.html', {'posted': request.POST}, status=400)

        InsumoModel.objects.create(nombre=nombre, unidad=unidad,
                                   stock_actual=stock_actual, stock_minimo=stock_minimo)
        messages.success(request, 'Insumo creado correctamente.')
        return redirect('admin_insumos')

    return render(request, 'admin/insumo_form.html', {'posted': None})


@admin_only
def insumo_edit_view(request, pk):
    try:
        insumo = InsumoModel.objects.get(pk=pk)
    except InsumoModel.DoesNotExist:
        messages.error(request, 'Insumo no encontrado.')
        return redirect('admin_insumos')

    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        unidad = (request.POST.get('unidad') or 'g').strip()
        try:
            stock_actual = float((request.POST.get('stock_actual') or '0').replace(',', '.'))
            stock_minimo = float((request.POST.get('stock_minimo') or '0').replace(',', '.'))
        except ValueError:
            messages.error(request, 'Los valores de stock deben ser números.')
            return render(request, 'admin/insumo_form.html',
                          {'posted': request.POST, 'insumo': insumo}, status=400)

        insumo.nombre = nombre
        insumo.unidad = unidad
        insumo.stock_actual = stock_actual
        insumo.stock_minimo = stock_minimo
        insumo.save()
        messages.success(request, 'Insumo actualizado.')
        return redirect('admin_insumos')

    return render(request, 'admin/insumo_form.html', {'insumo': insumo, 'posted': None})


@admin_only
def receta_view(request, producto_pk):
    try:
        producto = ProductoModel.objects.get(pk=producto_pk)
    except ProductoModel.DoesNotExist:
        messages.error(request, 'Producto no encontrado.')
        return redirect('admin_productos')

    insumos = InsumoModel.objects.all().order_by('nombre')
    receta = RecetaItemModel.objects.filter(producto=producto).select_related('insumo')

    if request.method == 'POST':
        RecetaItemModel.objects.filter(producto=producto).delete()
        insumo_ids = request.POST.getlist('insumo_id')
        cantidades = request.POST.getlist('cantidad')
        for iid, cant in zip(insumo_ids, cantidades):
            try:
                iid = int(iid)
                cant = float(cant.replace(',', '.'))
            except (ValueError, AttributeError):
                continue
            if cant > 0:
                RecetaItemModel.objects.create(producto=producto, insumo_id=iid, cantidad=cant)
        messages.success(request, f'Receta de «{producto.nombre}» guardada.')
        return redirect('admin_productos')

    return render(request, 'admin/receta_form.html',
                  {'producto': producto, 'insumos': insumos, 'receta': receta})


@admin_only
def reporte_reposicion_view(request):
    items = ReporteReposicionUseCase().execute()
    todos_insumos = InsumoModel.objects.all().order_by('nombre')
    return render(request, 'admin/reporte_reposicion.html',
                  {'items': items, 'todos_insumos': todos_insumos})
