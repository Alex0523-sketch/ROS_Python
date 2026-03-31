import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from django.utils import timezone

from users.domain.entities.reserva import Reserva


class CrearReservaUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, reserva_data: Dict[str, Any]) -> Reserva:
        fecha_reserva = reserva_data['fecha_reserva']
        if isinstance(fecha_reserva, str):
            fecha_reserva = datetime.fromisoformat(fecha_reserva.replace('Z', '+00:00'))
        if timezone.is_naive(fecha_reserva):
            fecha_reserva = timezone.make_aware(fecha_reserva, timezone.get_current_timezone())

        nombre = reserva_data.get('nombre_cliente', '') or ''
        if any(c.isdigit() for c in nombre):
            raise ValueError('El nombre no puede contener números.')

        if fecha_reserva < timezone.now():
            raise ValueError('No se puede realizar una reserva en una fecha pasada.')

        if reserva_data.get('numero_personas', 0) > 12:
            raise ValueError('Para grupos de más de 12 personas, por favor llame al restaurante.')

        codigo = (reserva_data.get('codigo_reserva') or '').strip() or f'RES-{uuid.uuid4().hex[:8].upper()}'

        reserva = Reserva(
            codigo_reserva=codigo,
            mesa_id=reserva_data['mesa_id'],
            fecha_reserva=fecha_reserva,
            hora=reserva_data['hora'],
            numero_personas=reserva_data['numero_personas'],
            estado=reserva_data.get('estado', 'PENDIENTE'),
            id=None,
            user_id=reserva_data.get('user_id'),
            nombre_cliente=reserva_data.get('nombre_cliente'),
            email_cliente=reserva_data.get('email_cliente'),
            telefono_cliente=reserva_data.get('telefono_cliente'),
            comentarios=reserva_data.get('comentarios'),
        )
        return self.reserva_repository.create(reserva)


class ObtenerReservaUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, reserva_id: int) -> Reserva:
        r = self.reserva_repository.get_by_id(reserva_id)
        if not r:
            raise LookupError('Reserva no encontrada.')
        return r


class ObtenerReservaPorCodigoUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, codigo: str) -> Optional[Reserva]:
        return self.reserva_repository.get_by_codigo(codigo)


class ListarReservasUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self) -> List[Reserva]:
        return self.reserva_repository.get_all()


class ListarReservasPorEstadoUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, estado: str) -> List[Reserva]:
        return self.reserva_repository.get_by_estado(estado)


class ActualizarReservaUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, reserva_id: int, reserva_data: Dict[str, Any]) -> Reserva:
        actual = self.reserva_repository.get_by_id(reserva_id)
        if not actual:
            raise LookupError('Reserva no encontrada.')

        fecha = reserva_data.get('fecha_reserva', actual.fecha_reserva)
        if isinstance(fecha, str):
            fecha = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
        if timezone.is_naive(fecha):
            fecha = timezone.make_aware(fecha, timezone.get_current_timezone())

        actualizado = Reserva(
            codigo_reserva=reserva_data.get('codigo_reserva', actual.codigo_reserva),
            mesa_id=reserva_data.get('mesa_id', actual.mesa_id),
            fecha_reserva=fecha,
            hora=reserva_data.get('hora', actual.hora),
            numero_personas=reserva_data.get('numero_personas', actual.numero_personas),
            estado=reserva_data.get('estado', actual.estado),
            id=actual.id,
            user_id=reserva_data.get('user_id', actual.user_id),
            nombre_cliente=reserva_data.get('nombre_cliente', actual.nombre_cliente),
            email_cliente=reserva_data.get('email_cliente', actual.email_cliente),
            telefono_cliente=reserva_data.get('telefono_cliente', actual.telefono_cliente),
            comentarios=reserva_data.get('comentarios', actual.comentarios),
            fecha_creacion=actual.fecha_creacion,
            fecha_actualizacion=actual.fecha_actualizacion,
        )
        return self.reserva_repository.update(reserva_id, actualizado)


class EliminarReservaUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, reserva_id: int) -> bool:
        if not self.reserva_repository.delete(reserva_id):
            raise LookupError('No se pudo eliminar la reserva (no existe).')
        return True


class CancelarReservaUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, codigo_reserva: str) -> Reserva:
        reserva = self.reserva_repository.get_by_codigo(codigo_reserva)
        if not reserva or reserva.id is None:
            raise LookupError('La reserva no existe.')

        reserva.estado = 'CANCELADO'
        return self.reserva_repository.update(reserva.id, reserva)
