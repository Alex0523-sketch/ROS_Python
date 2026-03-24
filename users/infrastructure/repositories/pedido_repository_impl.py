from users.domain.entities.pedido import Pedido
from users.infrastructure.models.pedido_model import PedidoModel


class PedidoRepositoryImpl:

    def _to_entity(self, model: PedidoModel) -> Pedido:
        return Pedido(
            id=model.id,
            user_id=model.user_id,
            cliente_nombre=model.cliente_nombre,
            numero_mesa=model.numero_mesa,
            reserva_id=model.reserva_id,
            empleado_id=model.empleado_asignado_id,
            comentarios=model.comentarios,
            total=model.total,
            estado=model.estado,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in PedidoModel.objects.all()]

    def get_by_id(self, pedido_id: int):
        try:
            return self._to_entity(PedidoModel.objects.get(pk=pedido_id))
        except PedidoModel.DoesNotExist:
            return None

    def get_by_estado(self, estado: str):
        return [self._to_entity(m) for m in PedidoModel.objects.filter(estado=estado)]

    def create(self, pedido: Pedido) -> Pedido:
        model = PedidoModel.objects.create(
            user_id=pedido.user_id,
            cliente_nombre=pedido.cliente_nombre,
            numero_mesa=pedido.numero_mesa,
            reserva_id=pedido.reserva_id,
            empleado_asignado_id=pedido.empleado_id,
            comentarios=pedido.comentarios,
            total=pedido.total,
            estado=pedido.estado,
        )
        return self._to_entity(model)

    def update(self, pedido_id: int, pedido: Pedido) -> Pedido:
        PedidoModel.objects.filter(pk=pedido_id).update(
            cliente_nombre=pedido.cliente_nombre,
            numero_mesa=pedido.numero_mesa,
            comentarios=pedido.comentarios,
            total=pedido.total,
            estado=pedido.estado,
        )
        return self.get_by_id(pedido_id)

    def delete(self, pedido_id: int) -> bool:
        deleted, _ = PedidoModel.objects.filter(pk=pedido_id).delete()
        return deleted > 0
