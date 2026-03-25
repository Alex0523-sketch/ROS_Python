from users.domain.entities.inventario import Inventario

class CrearInventarioUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self, producto_id, cantidad_disponible, cantidad_minima):
        if cantidad_disponible < 0 or cantidad_minima < 0:
            raise ValueError('Las cantidades no pueden ser negativas')

        inventario = Inventario(producto_id=producto_id, cantidad_disponible=cantidad_disponible, cantidad_minima=cantidad_minima)
        return self.inventario_repository.create(inventario)


class CrearOActualizarInventarioUseCase:
    """Si ya hay inventario para el producto, actualiza; si no, crea el registro en BD."""

    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self, producto_id: int, cantidad_disponible: int, cantidad_minima: int):
        if cantidad_disponible < 0 or cantidad_minima < 0:
            raise ValueError('Las cantidades no pueden ser negativas')

        rows = self.inventario_repository.get_by_producto(producto_id)
        if rows:
            inv = rows[0]
            inv.cantidad_disponible = cantidad_disponible
            inv.cantidad_minima = cantidad_minima
            return self.inventario_repository.update(inv.id, inv)

        nuevo = Inventario(
            producto_id=producto_id,
            cantidad_disponible=cantidad_disponible,
            cantidad_minima=cantidad_minima,
        )
        return self.inventario_repository.create(nuevo)


class ObtenerInventarioUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self, inventario_id):
        inventario = self.inventario_repository.get_by_id(inventario_id)
        if not inventario:
            raise LookupError('Inventario no encontrado')
        return inventario


class ListarInventarioUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self):
        return self.inventario_repository.get_all()


class AjustarStockInventarioUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self, producto_id, cantidad):
        inventarios = self.inventario_repository.get_by_producto(producto_id)
        if not inventarios:
            raise LookupError('No existe inventario para ese producto')

        inventario = inventarios[0]
        inventario.cantidad_disponible += cantidad

        if inventario.cantidad_disponible < 0:
            raise ValueError('Stock no puede ser negativo')

        if hasattr(self.inventario_repository, 'ajustar_stock'):
            return self.inventario_repository.ajustar_stock(producto_id, inventario.cantidad_disponible)

        return self.inventario_repository.update(inventario.id, inventario)


class ListarInventarioBajoStockUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self):
        if hasattr(self.inventario_repository, 'get_bajo_stock'):
            return self.inventario_repository.get_bajo_stock()
        return [i for i in self.inventario_repository.get_all() if i.cantidad_disponible <= i.cantidad_minima]


class ListarInventarioAgotadoUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self):
        if hasattr(self.inventario_repository, 'get_agotados'):
            return self.inventario_repository.get_agotados()
        return [i for i in self.inventario_repository.get_all() if i.cantidad_disponible == 0]


class EliminarInventarioUseCase:
    def __init__(self, inventario_repository):
        self.inventario_repository = inventario_repository

    def execute(self, inventario_id):
        if not self.inventario_repository.delete(inventario_id):
            raise LookupError('No se pudo eliminar inventario')
        return True
