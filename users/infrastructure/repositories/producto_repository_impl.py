from users.domain.entities.producto import Producto
from users.domain.repositories.producto_repository import ProductoRepository
from users.infrastructure.models.producto_model import ProductoModel


class ProductoRepositoryImpl(ProductoRepository):

    def _to_entity(self, model: ProductoModel) -> Producto:
        return Producto(
            nombre=model.nombre,
            precio=model.precio,
            categoria_id=model.categoria_id,
            id_producto=model.id_producto,
            descripcion=model.descripcion,
            imagen_url=model.imagen_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_all(self):
        return [self._to_entity(m) for m in ProductoModel.objects.all()]

    def get_by_id(self, producto_id: int):
        try:
            return self._to_entity(ProductoModel.objects.get(pk=producto_id))
        except ProductoModel.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str):
        nombre = (nombre or '').strip()
        if not nombre:
            return None
        qs = ProductoModel.objects.filter(nombre__iexact=nombre)
        if qs.exists():
            return self._to_entity(qs.first())
        return None

    def get_by_categoria(self, categoria_id: int):
        return [self._to_entity(m) for m in ProductoModel.objects.filter(categoria_id=categoria_id)]

    def create(self, producto: Producto) -> Producto:
        model = ProductoModel.objects.create(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            imagen_url=producto.imagen_url,
            categoria_id=producto.categoria_id,
        )
        return self._to_entity(model)

    def update(self, producto_id: int, producto: Producto) -> Producto:
        ProductoModel.objects.filter(pk=producto_id).update(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            imagen_url=producto.imagen_url,
            categoria_id=producto.categoria_id,
        )
        return self.get_by_id(producto_id)

    def delete(self, producto_id: int) -> bool:
        deleted, _ = ProductoModel.objects.filter(pk=producto_id).delete()
        return deleted > 0
