from users.domain.entities.inventario import Inventario
from users.domain.repositories.inventario_repository import InventarioRepository
from users.infrastructure.models.inventario_model import InventarioModel


class InventarioRepositoryImpl(InventarioRepository):

    def _to_entity(self, model: InventarioModel) -> Inventario:
        return Inventario(
            producto_id=model.producto_id,
            cantidad_disponible=model.cantidad_disponible,
            cantidad_minima=model.cantidad_minima,
            id=model.id,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in InventarioModel.objects.all()]

    def get_by_id(self, inventario_id: int):
        try:
            return self._to_entity(InventarioModel.objects.get(pk=inventario_id))
        except InventarioModel.DoesNotExist:
            return None

    def get_by_producto(self, producto_id: int):
        return [self._to_entity(m) for m in InventarioModel.objects.filter(producto_id=producto_id)]

    def create(self, inventario: Inventario) -> Inventario:
        model = InventarioModel.objects.create(
            producto_id=inventario.producto_id,
            cantidad_disponible=inventario.cantidad_disponible,
            cantidad_minima=inventario.cantidad_minima,
        )
        return self._to_entity(model)

    def update(self, inventario_id: int, inventario: Inventario) -> Inventario:
        InventarioModel.objects.filter(pk=inventario_id).update(
            cantidad_disponible=inventario.cantidad_disponible,
            cantidad_minima=inventario.cantidad_minima,
        )
        return self.get_by_id(inventario_id)

    def delete(self, inventario_id: int) -> bool:
        deleted, _ = InventarioModel.objects.filter(pk=inventario_id).delete()
        return deleted > 0
