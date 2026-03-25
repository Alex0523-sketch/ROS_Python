from datetime import datetime
from users.domain.entities.pago import Pago

class CrearPagoUseCase:
    def __init__(self, pago_repository):
        self.pago_repository = pago_repository

    def execute(self, pedido_id, metodo_pago, monto_total, estado='pendiente', user_id=None, fecha_pago=None):
        if monto_total <= 0:
            raise ValueError('Monto debe ser mayor que 0')

        pago = Pago(pedido_id=pedido_id, metodo_pago=metodo_pago, monto_total=monto_total, estado=estado, user_id=user_id, fecha_pago=fecha_pago or datetime.now())
        return self.pago_repository.create(pago)


class ObtenerPagoUseCase:
    def __init__(self, pago_repository):
        self.pago_repository = pago_repository

    def execute(self, pago_id):
        pago = self.pago_repository.get_by_id(pago_id)
        if not pago:
            raise LookupError('Pago no encontrado')
        return pago


class ListarPagosUseCase:
    def __init__(self, pago_repository):
        self.pago_repository = pago_repository

    def execute(self):
        return self.pago_repository.get_all()


class ConfirmarPagoUseCase:
    def __init__(self, pago_repository):
        self.pago_repository = pago_repository

    def execute(self, pago_id):
        pago = self.pago_repository.get_by_id(pago_id)
        if not pago:
            raise LookupError('Pago no encontrado')

        pago.estado = 'confirmado'
        pago.fecha_actualizacion = datetime.now()

        if hasattr(self.pago_repository, 'confirmar_pago'):
            return self.pago_repository.confirmar_pago(pago_id)

        return self.pago_repository.update(pago)


class RechazarPagoUseCase:
    def __init__(self, pago_repository):
        self.pago_repository = pago_repository

    def execute(self, pago_id):
        pago = self.pago_repository.get_by_id(pago_id)
        if not pago:
            raise LookupError('Pago no encontrado')

        pago.estado = 'rechazado'
        pago.fecha_actualizacion = datetime.now()

        if hasattr(self.pago_repository, 'rechazar_pago'):
            return self.pago_repository.rechazar_pago(pago_id)

        return self.pago_repository.update(pago)


class EliminarPagoUseCase:
    def __init__(self, pago_repository):
        self.pago_repository = pago_repository

    def execute(self, pago_id):
        if not self.pago_repository.delete(pago_id):
            raise LookupError('No se pudo eliminar pago')
        return True
