from django.db import transaction
from django.db.models import F

from users.infrastructure.models.detalle_pedido_model import DetallePedidoModel
from users.infrastructure.models.insumo_model import InsumoModel
from users.infrastructure.models.inventario_model import InventarioModel
from users.infrastructure.models.receta_item_model import RecetaItemModel


class CrearOActualizarInventarioUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self, producto_id: int, cantidad_disponible: int, cantidad_minima: int):
        obj, _ = InventarioModel.objects.update_or_create(
            producto_id=producto_id,
            defaults={
                'cantidad_disponible': cantidad_disponible,
                'cantidad_minima': cantidad_minima,
            },
        )
        return obj


class DescontarInventarioPorPedidoUseCase:
    """
    Dado un pedido_id, consulta sus detalles, busca la receta de cada producto
    y descuenta del stock de cada insumo la cantidad exacta.
    """

    @transaction.atomic
    def execute(self, pedido_id: int) -> dict:
        detalles = DetallePedidoModel.objects.filter(pedido_id=pedido_id).select_related('producto')
        movimientos = []
        sin_receta = []

        for detalle in detalles:
            receta_items = (
                RecetaItemModel.objects
                .filter(producto_id=detalle.producto_id)
                .select_related('insumo')
            )
            if not receta_items.exists():
                sin_receta.append(detalle.producto.nombre)
                continue

            for ri in receta_items:
                cantidad_a_descontar = ri.cantidad * detalle.cantidad
                insumo = InsumoModel.objects.select_for_update().get(pk=ri.insumo_id)
                nuevo_stock = max(0.0, insumo.stock_actual - cantidad_a_descontar)
                insumo.stock_actual = nuevo_stock
                insumo.save(update_fields=['stock_actual', 'fecha_actualizacion'])
                movimientos.append({
                    'insumo': insumo.nombre,
                    'descontado': cantidad_a_descontar,
                    'stock_restante': nuevo_stock,
                    'unidad': insumo.unidad,
                    'alerta': insumo.necesita_reposicion,
                })

        return {'movimientos': movimientos, 'sin_receta': sin_receta}


class ReporteReposicionUseCase:
    """Retorna todos los insumos cuyo stock_actual <= stock_minimo."""

    def execute(self) -> list:
        insumos = (
            InsumoModel.objects
            .filter(stock_actual__lte=F('stock_minimo'))
            .order_by('stock_actual')
        )
        return [
            {
                'id': i.pk,
                'nombre': i.nombre,
                'unidad': i.unidad,
                'stock_actual': i.stock_actual,
                'stock_minimo': i.stock_minimo,
                'faltante': round(max(0.0, i.stock_minimo - i.stock_actual), 2),
            }
            for i in insumos
        ]
