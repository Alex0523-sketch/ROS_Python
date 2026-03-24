from users.domain.entities.pago import Pago
from users.infrastructure.models.pago_model import PagoModel


class PagoRepositoryImpl:

    def _to_entity(self, model: PagoModel) -> Pago:
        return Pago(
            id=model.id,
            pedido_id=model.pedido_id,
            user_id=model.user_id,
            metodo_pago=model.metodo_pago,
            monto_total=model.monto_total,
            estado=model.estado,
            fecha_pago=model.fecha_pago,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in PagoModel.objects.all()]

    def get_by_id(self, pago_id: int):
        try:
            return self._to_entity(PagoModel.objects.get(pk=pago_id))
        except PagoModel.DoesNotExist:
            return None

    def get_by_pedido(self, pedido_id: int):
        return [self._to_entity(m) for m in PagoModel.objects.filter(pedido_id=pedido_id)]

    def create(self, pago: Pago) -> Pago:
        model = PagoModel.objects.create(
            pedido_id=pago.pedido_id,
            user_id=pago.user_id,
            metodo_pago=pago.metodo_pago,
            monto_total=pago.monto_total,
            estado=pago.estado,
            fecha_pago=pago.fecha_pago,
        )
        return self._to_entity(model)

    def update(self, pago_id: int, pago: Pago) -> Pago:
        PagoModel.objects.filter(pk=pago_id).update(
            metodo_pago=pago.metodo_pago,
            monto_total=pago.monto_total,
            estado=pago.estado,
            fecha_pago=pago.fecha_pago,
        )
        return self.get_by_id(pago_id)

    def delete(self, pago_id: int) -> bool:
        deleted, _ = PagoModel.objects.filter(pk=pago_id).delete()
        return deleted > 0
