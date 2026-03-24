from users.domain.entities.promocion import Promocion
from users.infrastructure.models.promocion_model import PromocionModel


class PromocionRepositoryImpl:

    def _to_entity(self, model: PromocionModel) -> Promocion:
        return Promocion(
            id_promocion=model.id_promocion,
            titulo=model.titulo,
            descripcion=model.descripcion,
            imagen_url=model.imagen_url,
            descuento=model.descuento,
            fecha_inicio=model.fecha_inicio,
            fecha_fin=model.fecha_fin,
            productos=list(model.productos.values_list('id_producto', flat=True)),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_all(self):
        return [self._to_entity(m) for m in PromocionModel.objects.prefetch_related('productos').all()]

    def get_by_id(self, promocion_id: int):
        try:
            return self._to_entity(PromocionModel.objects.prefetch_related('productos').get(pk=promocion_id))
        except PromocionModel.DoesNotExist:
            return None

    def create(self, promocion: Promocion) -> Promocion:
        model = PromocionModel.objects.create(
            titulo=promocion.titulo,
            descripcion=promocion.descripcion,
            imagen_url=promocion.imagen_url,
            descuento=promocion.descuento,
            fecha_inicio=promocion.fecha_inicio,
            fecha_fin=promocion.fecha_fin,
        )
        if promocion.productos:
            model.productos.set(promocion.productos)
        return self._to_entity(model)

    def update(self, promocion_id: int, promocion: Promocion) -> Promocion:
        PromocionModel.objects.filter(pk=promocion_id).update(
            titulo=promocion.titulo,
            descripcion=promocion.descripcion,
            imagen_url=promocion.imagen_url,
            descuento=promocion.descuento,
            fecha_inicio=promocion.fecha_inicio,
            fecha_fin=promocion.fecha_fin,
        )
        model = PromocionModel.objects.get(pk=promocion_id)
        if promocion.productos is not None:
            model.productos.set(promocion.productos)
        return self._to_entity(model)

    def delete(self, promocion_id: int) -> bool:
        deleted, _ = PromocionModel.objects.filter(pk=promocion_id).delete()
        return deleted > 0
