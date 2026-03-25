from users.domain.entities.horario import Horario
from users.domain.repositories.horario_repository import HorarioRepository
from users.infrastructure.models.horario_model import HorarioModel


class HorarioRepositoryImpl(HorarioRepository):

    def _to_entity(self, model: HorarioModel) -> Horario:
        return Horario(
            user_id=model.user_id,
            dia_semana=model.dia_semana,
            hora_inicio=model.hora_inicio,
            hora_fin=model.hora_fin,
            id=model.id,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in HorarioModel.objects.all()]

    def get_by_id(self, horario_id: int):
        try:
            return self._to_entity(HorarioModel.objects.get(pk=horario_id))
        except HorarioModel.DoesNotExist:
            return None

    def get_by_user(self, user_id: int):
        return [self._to_entity(m) for m in HorarioModel.objects.filter(user_id=user_id)]

    def create(self, horario: Horario) -> Horario:
        model = HorarioModel.objects.create(
            user_id=horario.user_id,
            dia_semana=horario.dia_semana,
            hora_inicio=horario.hora_inicio,
            hora_fin=horario.hora_fin,
        )
        return self._to_entity(model)

    def update(self, horario_id: int, horario: Horario) -> Horario:
        HorarioModel.objects.filter(pk=horario_id).update(
            dia_semana=horario.dia_semana,
            hora_inicio=horario.hora_inicio,
            hora_fin=horario.hora_fin,
        )
        return self.get_by_id(horario_id)

    def delete(self, horario_id: int) -> bool:
        deleted, _ = HorarioModel.objects.filter(pk=horario_id).delete()
        return deleted > 0
