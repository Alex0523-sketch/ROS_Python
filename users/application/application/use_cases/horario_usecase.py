from users.domain.entities.horario import Horario

class CrearHorarioUseCase:
    def __init__(self, horario_repository):
        self.horario_repository = horario_repository

    def execute(self, user_id, dia_semana, hora_inicio, hora_fin):
        if not (user_id and dia_semana and hora_inicio and hora_fin):
            raise ValueError('Todos los campos son obligatorios')

        horario = Horario(user_id=user_id, dia_semana=dia_semana, hora_inicio=hora_inicio, hora_fin=hora_fin)
        return self.horario_repository.create(horario)


class ObtenerHorarioUseCase:
    def __init__(self, horario_repository):
        self.horario_repository = horario_repository

    def execute(self, horario_id):
        horario = self.horario_repository.get_by_id(horario_id)
        if not horario:
            raise LookupError('Horario no encontrado')
        return horario


class ListarHorariosUsuarioUseCase:
    def __init__(self, horario_repository):
        self.horario_repository = horario_repository

    def execute(self, user_id):
        return self.horario_repository.get_by_user(user_id)


class ActualizarHorarioUseCase:
    def __init__(self, horario_repository):
        self.horario_repository = horario_repository

    def execute(self, horario_id, dia_semana=None, hora_inicio=None, hora_fin=None):
        horario = self.horario_repository.get_by_id(horario_id)
        if not horario:
            raise LookupError('Horario no encontrado')

        horario.dia_semana = dia_semana or horario.dia_semana
        horario.hora_inicio = hora_inicio or horario.hora_inicio
        horario.hora_fin = hora_fin or horario.hora_fin

        return self.horario_repository.update(horario)


class EliminarHorarioUseCase:
    def __init__(self, horario_repository):
        self.horario_repository = horario_repository

    def execute(self, horario_id):
        if not self.horario_repository.delete(horario_id):
            raise LookupError('No se pudo eliminar horario')
        return True
