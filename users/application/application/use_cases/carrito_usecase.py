from users.domain.entities.carrito_item import CarritoItem

class AgregarItemCarritoUseCase:
    def __init__(self, carrito_repository):
        self.carrito_repository = carrito_repository

    def execute(self, usuario_id, producto_id, nombre, precio, cantidad):
        if cantidad <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')

        item_existente = self.carrito_repository.get_by_producto(usuario_id, producto_id)
        if item_existente:
            item_existente.cantidad += cantidad
            item_existente.calcular_subtotal()
            return self.carrito_repository.update(item_existente)

        item = CarritoItem(producto_id=producto_id, nombre=nombre, precio=precio, cantidad=cantidad)
        return self.carrito_repository.create(item)


class ObtenerItemCarritoUseCase:
    def __init__(self, carrito_repository):
        self.carrito_repository = carrito_repository

    def execute(self, item_id):
        item = self.carrito_repository.get_by_id(item_id)
        if not item:
            raise LookupError('Item de carrito no encontrado')
        return item


class ListarCarritoUsuarioUseCase:
    def __init__(self, carrito_repository):
        self.carrito_repository = carrito_repository

    def execute(self, usuario_id):
        return self.carrito_repository.get_by_usuario(usuario_id)


class EliminarItemCarritoUseCase:
    def __init__(self, carrito_repository):
        self.carrito_repository = carrito_repository

    def execute(self, item_id):
        if not self.carrito_repository.delete(item_id):
            raise LookupError('No se pudo eliminar el ítem, no existe')
        return True


class VaciarCarritoUsuarioUseCase:
    def __init__(self, carrito_repository):
        self.carrito_repository = carrito_repository

    def execute(self, usuario_id):
        return self.carrito_repository.delete_by_usuario(usuario_id)


class CalcularTotalCarritoUseCase:
    def __init__(self, carrito_repository):
        self.carrito_repository = carrito_repository

    def execute(self, usuario_id):
        return self.carrito_repository.calcular_total(usuario_id)
