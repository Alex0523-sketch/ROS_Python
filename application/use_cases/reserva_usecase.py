# application/use_cases/reserva_usecases.py
import uuid
from datetime import datetime

class CrearReservaUseCase:
    def __init__(self, reserva_repository):
         
        self.reserva_repository = reserva_repository

    def execute(self, reserva_data: dict):

        if reserva_data['fecha_reserva'] < datetime.now():
            raise ValueError("No se puede realizar una reserva en una fecha pasada.")


        if reserva_data['numero_personas'] > 12:
            raise ValueError("Para grupos de más de 12 personas, por favor llame al restaurante.")


        if not reserva_data.get('codigo_reserva'):
            reserva_data['codigo_reserva'] = f"RES-{uuid.uuid4().hex[:8].upper()}"

        reserva_data['estado'] = "PENDIENTE"

        
        return self.reserva_repository.save(reserva_data)

class CancelarReservaUseCase:
    def __init__(self, reserva_repository):
        self.reserva_repository = reserva_repository

    def execute(self, codigo_reserva: str):
        reserva = self.reserva_repository.get_by_codigo(codigo_reserva)
        if not reserva:
            raise Exception("La reserva no existe.")
        
        
        reserva.estado = "CANCELADO"
        return self.reserva_repository.update(reserva)
