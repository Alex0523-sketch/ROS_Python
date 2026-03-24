from users.domain.entities.detalle_pedido import DetallePedido
from users.infrastructure.models.detalle_pedido_model import DetallePedidoModel


class DetallePedidoRepositoryImpl:

    def _to_entity(self, model: DetallePedidoModel) -> DetallePedido:
        return DetallePedido(
            id=model.id,
            pedido_id=model.pedido_id,
            producto_id=model.producto_id,
            cantidad=model.cantidad,
            precio=model.precio,
        )

    def get_all(self):
        return [self._to_entity(m) for m in DetallePedidoModel.objects.all()]

    def get_by_id(self, detalle_id: int):
        try:
            return self._to_entity(DetallePedidoModel.objects.get(pk=detalle_id))
        except DetallePedidoModel.DoesNotExist:
            return None

    def get_by_pedido(self, pedido_id: int):
        return [self._to_entity(m) for m in DetallePedidoModel.objects.filter(pedido_id=pedido_id)]

    def create(self, detalle: DetallePedido) -> DetallePedido:
        model = DetallePedidoModel.objects.create(
            pedido_id=detalle.pedido_id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio=detalle.precio,
        )
        return self._to_entity(model)

    def update(self, detalle_id: int, detalle: DetallePedido) -> DetallePedido:
        DetallePedidoModel.objects.filter(pk=detalle_id).update(
            cantidad=detalle.cantidad,
            precio=detalle.precio,
        )
        return self.get_by_id(detalle_id)

    def delete(self, detalle_id: int) -> bool:
        deleted, _ = DetallePedidoModel.objects.filter(pk=detalle_id).delete()
        return deleted > 0
