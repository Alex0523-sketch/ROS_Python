from django.db import transaction
from django.db.models import F

from users.domain.entities.insumo import Insumo, RecetaItem
from users.domain.repositories.insumo_repository import InsumoRepository, RecetaRepository
from users.infrastructure.models.insumo_model import InsumoModel
from users.infrastructure.models.receta_item_model import RecetaItemModel


class InsumoRepositoryImpl(InsumoRepository):

    def _to_entity(self, m: InsumoModel) -> Insumo:
        return Insumo(id=m.pk, nombre=m.nombre, unidad=m.unidad,
                      stock_actual=m.stock_actual, stock_minimo=m.stock_minimo)

    def get_all(self):
        return [self._to_entity(m) for m in InsumoModel.objects.all().order_by('nombre')]

    def get_by_id(self, insumo_id):
        try:
            return self._to_entity(InsumoModel.objects.get(pk=insumo_id))
        except InsumoModel.DoesNotExist:
            return None

    def create(self, insumo: Insumo) -> Insumo:
        m = InsumoModel.objects.create(
            nombre=insumo.nombre, unidad=insumo.unidad,
            stock_actual=insumo.stock_actual, stock_minimo=insumo.stock_minimo,
        )
        return self._to_entity(m)

    def update_stock(self, insumo_id: int, nuevo_stock: float) -> None:
        InsumoModel.objects.filter(pk=insumo_id).update(stock_actual=nuevo_stock)

    def get_bajo_minimo(self):
        qs = InsumoModel.objects.filter(stock_actual__lte=F('stock_minimo')).order_by('stock_actual')
        return [self._to_entity(m) for m in qs]


class RecetaRepositoryImpl(RecetaRepository):

    def get_by_producto(self, producto_id: int):
        qs = RecetaItemModel.objects.filter(producto_id=producto_id).select_related('insumo')
        return [
            RecetaItem(id=m.pk, producto_id=m.producto_id, insumo_id=m.insumo_id,
                       cantidad=m.cantidad, insumo_nombre=m.insumo.nombre, insumo_unidad=m.insumo.unidad)
            for m in qs
        ]

    def create(self, item: RecetaItem) -> RecetaItem:
        m = RecetaItemModel.objects.create(
            producto_id=item.producto_id, insumo_id=item.insumo_id, cantidad=item.cantidad,
        )
        return RecetaItem(id=m.pk, producto_id=m.producto_id, insumo_id=m.insumo_id, cantidad=m.cantidad)

    @transaction.atomic
    def delete_by_producto(self, producto_id: int) -> None:
        RecetaItemModel.objects.filter(producto_id=producto_id).delete()
