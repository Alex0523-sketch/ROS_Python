from users.domain.entities.detalle_pago import DetallePago
from users.domain.repositories.detalle_pago_repository import DetallePagoRepository
from users.infrastructure.models.detalle_pago_model import DetallePagoModel


class DetallePagoRepositoryImpl(DetallePagoRepository):

    def _to_entity(self, model: DetallePagoModel) -> DetallePago:
        return DetallePago(
            pago_id=model.pago_id,
            monto=model.monto,
            id=model.id,
            descripcion=model.descripcion,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in DetallePagoModel.objects.all()]

    def get_by_id(self, detalle_id: int):
        try:
            return self._to_entity(DetallePagoModel.objects.get(pk=detalle_id))
        except DetallePagoModel.DoesNotExist:
            return None

    def get_by_pago(self, pago_id: int):
        return [self._to_entity(m) for m in DetallePagoModel.objects.filter(pago_id=pago_id)]

    def create(self, detalle: DetallePago) -> DetallePago:
        model = DetallePagoModel.objects.create(
            pago_id=detalle.pago_id,
            monto=detalle.monto,
            descripcion=detalle.descripcion,
        )
        return self._to_entity(model)

    def update(self, detalle_id: int, detalle: DetallePago) -> DetallePago:
        DetallePagoModel.objects.filter(pk=detalle_id).update(
            monto=detalle.monto,
            descripcion=detalle.descripcion,
        )
        return self.get_by_id(detalle_id)

    def delete(self, detalle_id: int) -> bool:
        deleted, _ = DetallePagoModel.objects.filter(pk=detalle_id).delete()
        return deleted > 0
