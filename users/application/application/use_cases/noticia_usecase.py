from datetime import datetime
from users.domain.entities.noticia import Noticia

class CrearNoticiaUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self, titulo, contenido, imagen=None, fecha_publicacion=None):
        if not titulo or not contenido:
            raise ValueError('Título y contenido son obligatorios')

        noticia = Noticia(titulo=titulo, contenido=contenido, imagen=imagen, fecha_publicacion=fecha_publicacion or datetime.now())
        return self.noticia_repository.create(noticia)


class ObtenerNoticiaUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self, noticia_id):
        noticia = self.noticia_repository.get_by_id(noticia_id)
        if not noticia:
            raise LookupError('Noticia no encontrada')
        return noticia


class ListarNoticiasUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self):
        return self.noticia_repository.get_all()


class ListarNoticiasRecientesUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self, limite=10):
        if hasattr(self.noticia_repository, 'get_recientes'):
            return self.noticia_repository.get_recientes(limite)
        todas = self.noticia_repository.get_all()
        return sorted(todas, key=lambda x: x.fecha_actualizacion or datetime.min, reverse=True)[:limite]


class BuscarNoticiasPorTituloUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self, texto):
        if hasattr(self.noticia_repository, 'buscar_por_titulo'):
            return self.noticia_repository.buscar_por_titulo(texto)
        return [n for n in self.noticia_repository.get_all() if texto.lower() in n.titulo.lower()]


class ActualizarNoticiaUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self, noticia_id, titulo=None, contenido=None, imagen=None, fecha_publicacion=None):
        noticia = self.noticia_repository.get_by_id(noticia_id)
        if not noticia:
            raise LookupError('Noticia no encontrada')

        noticia.titulo = titulo or noticia.titulo
        noticia.contenido = contenido or noticia.contenido
        noticia.imagen = imagen if imagen is not None else noticia.imagen
        noticia.fecha_publicacion = fecha_publicacion or noticia.fecha_publicacion

        return self.noticia_repository.update(noticia)


class EliminarNoticiaUseCase:
    def __init__(self, noticia_repository):
        self.noticia_repository = noticia_repository

    def execute(self, noticia_id):
        if not self.noticia_repository.delete(noticia_id):
            raise LookupError('No se pudo eliminar noticia')
        return True
