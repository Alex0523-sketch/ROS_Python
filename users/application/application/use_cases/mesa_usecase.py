from users.domain.entities.mesa import Mesa

class CrearMesaUseCase:
    def __init__(self, mesa_repository):
        self.mesa_repository = mesa_repository

    def execute(self, numero_mesa, capacidad, estado='libre', ubicacion=None):
        if capacidad <= 0:
            raise ValueError('Capacidad debe ser mayor que 0')

        mesa = Mesa(numero_mesa=numero_mesa, capacidad=capacidad, estado=estado, ubicacion=ubicacion)
        return self.mesa_repository.create(mesa)


class ObtenerMesaUseCase:
    def __init__(self, mesa_repository):
        self.mesa_repository = mesa_repository

    def execute(self, mesa_id):
        mesa = self.mesa_repository.get_by_id(mesa_id)
        if not mesa:
            raise LookupError('Mesa no encontrada')
        return mesa


class ListarMesasUseCase:
    def __init__(self, mesa_repository):
        self.mesa_repository = mesa_repository

    def execute(self):
        return self.mesa_repository.get_all()


class ListarMesasDisponiblesUseCase:
    def __init__(self, mesa_repository):
        self.mesa_repository = mesa_repository

    def execute(self, fecha=None, hora=None, personas=None):
        if hasattr(self.mesa_repository, 'get_disponibles') and fecha and hora and personas is not None:
            return self.mesa_repository.get_disponibles(fecha, hora, personas)
        return self.mesa_repository.get_by_estado('libre')


class ActualizarMesaUseCase:
    def __init__(self, mesa_repository):
        self.mesa_repository = mesa_repository

    def execute(self, mesa_id, numero_mesa=None, capacidad=None, estado=None, ubicacion=None):
        mesa = self.mesa_repository.get_by_id(mesa_id)
        if not mesa:
            raise LookupError('Mesa no encontrada')

        mesa.numero_mesa = numero_mesa if numero_mesa is not None else mesa.numero_mesa
        mesa.capacidad = capacidad if capacidad is not None else mesa.capacidad
        mesa.estado = estado if estado is not None else mesa.estado
        mesa.ubicacion = ubicacion if ubicacion is not None else mesa.ubicacion

        return self.mesa_repository.update(mesa)


class EliminarMesaUseCase:
    def __init__(self, mesa_repository):
        self.mesa_repository = mesa_repository

    def execute(self, mesa_id):
        if not self.mesa_repository.delete(mesa_id):
            raise LookupError('No se pudo eliminar mesa')
        return True
