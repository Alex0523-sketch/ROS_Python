from users.domain.entities.detalle_pedido import DetallePedido

class AgregarDetallePedidoUseCase:
    def __init__(self, detalle_pedido_repository):
        self.detalle_pedido_repository = detalle_pedido_repository

    def execute(self, pedido_id, producto_id, cantidad, precio):
        if cantidad <= 0 or precio <= 0:
            raise ValueError('Cantidad y precio deben ser mayores que 0')

        detalle = DetallePedido(pedido_id=pedido_id, producto_id=producto_id, cantidad=cantidad, precio=precio)
        return self.detalle_pedido_repository.create(detalle)


class ListarDetallesPedidoUseCase:
    def __init__(self, detalle_pedido_repository):
        self.detalle_pedido_repository = detalle_pedido_repository

    def execute(self, pedido_id=None):
        if pedido_id is None:
            return self.detalle_pedido_repository.get_all()
        return self.detalle_pedido_repository.get_by_pedido(pedido_id)


class CalcularSubtotalPedidoUseCase:
    def __init__(self, detalle_pedido_repository):
        self.detalle_pedido_repository = detalle_pedido_repository

    def execute(self, pedido_id):
        if hasattr(self.detalle_pedido_repository, 'calcular_subtotal'):
            return self.detalle_pedido_repository.calcular_subtotal(pedido_id)

        detalles = self.detalle_pedido_repository.get_by_pedido(pedido_id)
        return sum([d.calcular_subtotal() for d in detalles])


class ActualizarDetallePedidoUseCase:
    def __init__(self, detalle_pedido_repository):
        self.detalle_pedido_repository = detalle_pedido_repository

    def execute(self, detalle_id, cantidad=None, precio=None):
        detalle = self.detalle_pedido_repository.get_by_id(detalle_id)
        if not detalle:
            raise LookupError('Detalle de pedido no encontrado')

        if cantidad is not None and cantidad <= 0:
            raise ValueError('Cantidad debe ser mayor a 0')
        if precio is not None and precio <= 0:
            raise ValueError('Precio debe ser mayor a 0')

        detalle.cantidad = cantidad if cantidad is not None else detalle.cantidad
        detalle.precio = precio if precio is not None else detalle.precio

        return self.detalle_pedido_repository.update(detalle)


class EliminarDetallePedidoUseCase:
    def __init__(self, detalle_pedido_repository):
        self.detalle_pedido_repository = detalle_pedido_repository

    def execute(self, detalle_id):
        if not self.detalle_pedido_repository.delete(detalle_id):
            raise LookupError('No se pudo eliminar detalle de pedido')
        return True
