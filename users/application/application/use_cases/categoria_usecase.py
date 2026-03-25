from users.domain.entities.categoria import Categoria

class CrearCategoriaUseCase:
    def __init__(self, categoria_repository):
        self.categoria_repository = categoria_repository

    def execute(self, nombre, descripcion=None):
        if not nombre:
            raise ValueError('El nombre de categoría es obligatorio')

        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        if hasattr(self.categoria_repository, 'create'):
            return self.categoria_repository.create(categoria)
        return self.categoria_repository.save(categoria)


class ObtenerCategoriaUseCase:
    def __init__(self, categoria_repository):
        self.categoria_repository = categoria_repository

    def execute(self, categoria_id):
        categoria = self.categoria_repository.get_by_id(categoria_id)
        if not categoria:
            raise LookupError('Categoría no encontrada')
        return categoria


class ListarCategoriasUseCase:
    def __init__(self, categoria_repository):
        self.categoria_repository = categoria_repository

    def execute(self):
        return self.categoria_repository.get_all()


class ActualizarCategoriaUseCase:
    def __init__(self, categoria_repository):
        self.categoria_repository = categoria_repository

    def execute(self, categoria_id, nombre=None, descripcion=None):
        categoria = self.categoria_repository.get_by_id(categoria_id)
        if not categoria:
            raise LookupError('Categoría no encontrada')

        categoria.nombre = nombre or categoria.nombre
        categoria.descripcion = descripcion if descripcion is not None else categoria.descripcion

        if hasattr(self.categoria_repository, 'update'):
            return self.categoria_repository.update(categoria_id, categoria)
        raise AttributeError('Repositorio no soporta update')


class EliminarCategoriaUseCase:
    def __init__(self, categoria_repository):
        self.categoria_repository = categoria_repository

    def execute(self, categoria_id):
        if not self.categoria_repository.delete(categoria_id):
            raise LookupError('No se pudo eliminar la categoría')
        return True
