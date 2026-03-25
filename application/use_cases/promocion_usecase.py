from datetime import date, datetime
from users.domain.entities.promocion import Promocion

class CrearPromocionUseCase:
    def __init__(self, promocion_repository):
        self.promocion_repository = promocion_repository

    def execute(self, titulo, descuento, fecha_inicio, fecha_fin, descripcion=None, imagen_url=None, productos=None):
        if descuento <= 0 or descuento > 100:
            raise ValueError('Descuento debe estar entre 0 y 100')
        if fecha_fin < fecha_inicio:
            raise ValueError('Fecha fin debe ser posterior a fecha inicio')

        promocion = Promocion(titulo=titulo, descuento=descuento, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, descripcion=descripcion, imagen_url=imagen_url, productos=productos or [])
        return self.promocion_repository.create(promocion)


class ObtenerPromocionUseCase:
    def __init__(self, promocion_repository):
        self.promocion_repository = promocion_repository

    def execute(self, promocion_id):
        promocion = self.promocion_repository.get_by_id(promocion_id)
        if not promocion:
            raise LookupError('Promoción no encontrada')
        return promocion


class ListarPromocionesUseCase:
    def __init__(self, promocion_repository):
        self.promocion_repository = promocion_repository

    def execute(self):
        return self.promocion_repository.get_all()


class ListarPromocionesVigentesUseCase:
    def __init__(self, promocion_repository):
        self.promocion_repository = promocion_repository

    def execute(self, fecha=None):
        fecha = fecha or date.today()
        if hasattr(self.promocion_repository, 'get_vigentes'):
            return self.promocion_repository.get_vigentes()

        return [p for p in self.promocion_repository.get_all() if p.fecha_inicio <= fecha <= p.fecha_fin]


class ActualizarPromocionUseCase:
    def __init__(self, promocion_repository):
        self.promocion_repository = promocion_repository

    def execute(self, promocion_id, **kwargs):
        promocion = self.promocion_repository.get_by_id(promocion_id)
        if not promocion:
            raise LookupError('Promoción no encontrada')

        for key, value in kwargs.items():
            if hasattr(promocion, key) and value is not None:
                setattr(promocion, key, value)

        return self.promocion_repository.update(promocion)


class EliminarPromocionUseCase:
    def __init__(self, promocion_repository):
        self.promocion_repository = promocion_repository

    def execute(self, promocion_id):
        if not self.promocion_repository.delete(promocion_id):
            raise LookupError('No se pudo eliminar promoción')
        return True
