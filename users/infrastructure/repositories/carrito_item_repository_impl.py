from users.domain.entities.carrito_item import CarritoItem
from users.domain.repositories.carrito_item_repository import CarritoItemRepository
from users.infrastructure.models.carrito_item_model import CarritoItemModel


class CarritoItemRepositoryImpl(CarritoItemRepository):

    def _to_entity(self, model: CarritoItemModel) -> CarritoItem:
        return CarritoItem(
            producto_id=model.producto_id,
            nombre=model.nombre,
            precio=model.precio,
            cantidad=model.cantidad,
            subtotal=model.subtotal,
        )

    def get_all(self):
        return [self._to_entity(m) for m in CarritoItemModel.objects.all()]

    def get_by_id(self, item_id: int):
        try:
            return self._to_entity(CarritoItemModel.objects.get(pk=item_id))
        except CarritoItemModel.DoesNotExist:
            return None

    def create(self, item: CarritoItem) -> CarritoItem:
        model = CarritoItemModel.objects.create(
            producto_id=item.producto_id,
            nombre=item.nombre,
            precio=item.precio,
            cantidad=item.cantidad,
            subtotal=item.subtotal,
        )
        return self._to_entity(model)

    def update(self, item_id: int, item: CarritoItem) -> CarritoItem:
        CarritoItemModel.objects.filter(pk=item_id).update(
            nombre=item.nombre,
            precio=item.precio,
            cantidad=item.cantidad,
            subtotal=item.precio * item.cantidad,
        )
        return self.get_by_id(item_id)

    def delete(self, item_id: int) -> bool:
        deleted, _ = CarritoItemModel.objects.filter(pk=item_id).delete()
        return deleted > 0
