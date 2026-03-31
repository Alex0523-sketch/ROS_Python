from users.domain.entities.noticia import Noticia
from users.domain.repositories.noticia_repository import NoticiaRepository
from users.infrastructure.models.noticia_model import NoticiaModel


class NoticiaRepositoryImpl(NoticiaRepository):

    def _to_entity(self, model: NoticiaModel) -> Noticia:
        return Noticia(
            titulo=model.titulo,
            contenido=model.contenido,
            id=model.id,
            imagen=model.imagen,
            fecha_publicacion=model.fecha_publicacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in NoticiaModel.objects.all()]

    def get_by_id(self, noticia_id: int):
        try:
            return self._to_entity(NoticiaModel.objects.get(pk=noticia_id))
        except NoticiaModel.DoesNotExist:
            return None

    def create(self, noticia: Noticia) -> Noticia:
        model = NoticiaModel.objects.create(
            titulo=noticia.titulo,
            contenido=noticia.contenido,
            imagen=noticia.imagen,
            fecha_publicacion=noticia.fecha_publicacion,
        )
        return self._to_entity(model)

    def update(self, noticia_id: int, noticia: Noticia) -> Noticia:
        NoticiaModel.objects.filter(pk=noticia_id).update(
            titulo=noticia.titulo,
            contenido=noticia.contenido,
            imagen=noticia.imagen,
            fecha_publicacion=noticia.fecha_publicacion,
        )
        return self.get_by_id(noticia_id)

    def delete(self, noticia_id: int) -> bool:
        deleted, _ = NoticiaModel.objects.filter(pk=noticia_id).delete()
        return deleted > 0
