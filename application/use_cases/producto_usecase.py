from users.domain.entities.producto import Producto


class CrearProductoUseCase:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def execute(self, producto_data: dict):
        if not producto_data.get("nombre"):
            raise ValueError("El nombre del producto es obligatorio.")

        if producto_data.get("precio", 0) <= 0:
            raise ValueError("El precio debe ser mayor que 0.")

        existentes = self.producto_repository.get_by_nombre(producto_data["nombre"])
        if existentes:
            raise ValueError("Ya existe un producto con ese nombre.")

        producto = Producto(
            nombre=producto_data["nombre"],
            descripcion=producto_data.get("descripcion"),
            precio=producto_data["precio"],
            imagen_url=producto_data.get("imagen_url"),
            categoria_id=producto_data["categoria_id"],
        )

        if hasattr(self.producto_repository, "create"):
            return self.producto_repository.create(producto)

        return self.producto_repository.save(producto)


class ObtenerProductoUseCase:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def execute(self, producto_id: int):
        producto = self.producto_repository.get_by_id(producto_id)
        if not producto:
            raise LookupError("Producto no encontrado.")
        return producto


class ListarProductosUseCase:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def execute(self):
        return self.producto_repository.get_all()


class ActualizarProductoUseCase:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def execute(self, producto_id: int, producto_data: dict):
        producto_existente = self.producto_repository.get_by_id(producto_id)
        if not producto_existente:
            raise LookupError("Producto no existe.")

        if producto_data.get("precio") is not None and producto_data.get("precio") <= 0:
            raise ValueError("El precio debe ser mayor que 0.")

        producto_actualizado = Producto(
            id_producto=producto_existente.id_producto,
            nombre=producto_data.get("nombre", producto_existente.nombre),
            descripcion=producto_data.get("descripcion", producto_existente.descripcion),
            precio=producto_data.get("precio", producto_existente.precio),
            imagen_url=producto_data.get("imagen_url", producto_existente.imagen_url),
            categoria_id=producto_data.get("categoria_id", producto_existente.categoria_id),
        )

        if hasattr(self.producto_repository, "update"):
            # Implementation sometimes expects (id, entity)
            try:
                return self.producto_repository.update(producto_id, producto_actualizado)
            except TypeError:
                return self.producto_repository.update(producto_actualizado)

        raise AttributeError("Repositorio no soporta actualización de producto")


class EliminarProductoUseCase:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def execute(self, producto_id: int):
        eliminado = self.producto_repository.delete(producto_id)
        if not eliminado:
            raise LookupError("No se pudo eliminar el producto (no existe).")
        return True
