from users.domain.entities.categoria import Categoria
from users.infrastructure.models.categoria_model import CategoriaModel


class CategoriaRepositoryImpl:

    def _to_entity(self, model: CategoriaModel) -> Categoria:
        return Categoria(
            id_categoria=model.id_categoria,
            nombre=model.nombre,
            descripcion=model.descripcion,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_all(self):
        return [self._to_entity(m) for m in CategoriaModel.objects.all()]

    def get_by_id(self, categoria_id: int):
        try:
            return self._to_entity(CategoriaModel.objects.get(pk=categoria_id))
        except CategoriaModel.DoesNotExist:
            return None

    def create(self, categoria: Categoria) -> Categoria:
        model = CategoriaModel.objects.create(
            nombre=categoria.nombre,
            descripcion=categoria.descripcion,
        )
        return self._to_entity(model)

    def update(self, categoria_id: int, categoria: Categoria) -> Categoria:
        CategoriaModel.objects.filter(pk=categoria_id).update(
            nombre=categoria.nombre,
            descripcion=categoria.descripcion,
        )
        return self.get_by_id(categoria_id)

    def delete(self, categoria_id: int) -> bool:
        deleted, _ = CategoriaModel.objects.filter(pk=categoria_id).delete()
        return deleted > 0
