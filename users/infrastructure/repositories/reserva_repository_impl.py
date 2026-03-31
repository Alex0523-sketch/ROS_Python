from users.domain.entities.reserva import Reserva
from users.domain.repositories.reserva_repository import ReservaRepository
from users.infrastructure.models.reserva_model import ReservaModel


class ReservaRepositoryImpl(ReservaRepository):

    def _to_entity(self, model: ReservaModel) -> Reserva:
        return Reserva(
            codigo_reserva=model.codigo_reserva or '',
            mesa_id=model.mesa_id,
            fecha_reserva=model.fecha_reserva,
            hora=model.hora,
            numero_personas=model.numero_personas,
            estado=model.estado,
            id=model.id,
            user_id=model.user_id,
            nombre_cliente=model.nombre_cliente,
            email_cliente=model.email_cliente,
            telefono_cliente=model.telefono_cliente,
            comentarios=model.comentarios,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in ReservaModel.objects.all()]

    def get_by_id(self, reserva_id: int):
        try:
            return self._to_entity(ReservaModel.objects.get(pk=reserva_id))
        except ReservaModel.DoesNotExist:
            return None

    def get_by_codigo(self, codigo: str):
        if not codigo:
            return None
        try:
            return self._to_entity(ReservaModel.objects.get(codigo_reserva=codigo.strip()))
        except ReservaModel.DoesNotExist:
            return None

    def get_by_estado(self, estado: str):
        return [self._to_entity(m) for m in ReservaModel.objects.filter(estado=estado)]

    def create(self, reserva: Reserva) -> Reserva:
        model = ReservaModel.objects.create(
            codigo_reserva=reserva.codigo_reserva,
            user_id=reserva.user_id,
            nombre_cliente=reserva.nombre_cliente,
            email_cliente=reserva.email_cliente,
            telefono_cliente=reserva.telefono_cliente,
            mesa_id=reserva.mesa_id,
            fecha_reserva=reserva.fecha_reserva,
            hora=reserva.hora,
            numero_personas=reserva.numero_personas,
            estado=reserva.estado,
            comentarios=reserva.comentarios,
        )
        return self._to_entity(model)

    def update(self, reserva_id: int, reserva: Reserva) -> Reserva:
        ReservaModel.objects.filter(pk=reserva_id).update(
            nombre_cliente=reserva.nombre_cliente,
            email_cliente=reserva.email_cliente,
            telefono_cliente=reserva.telefono_cliente,
            mesa_id=reserva.mesa_id,
            fecha_reserva=reserva.fecha_reserva,
            hora=reserva.hora,
            numero_personas=reserva.numero_personas,
            estado=reserva.estado,
            comentarios=reserva.comentarios,
        )
        return self.get_by_id(reserva_id)

    def delete(self, reserva_id: int) -> bool:
        deleted, _ = ReservaModel.objects.filter(pk=reserva_id).delete()
        return deleted > 0
