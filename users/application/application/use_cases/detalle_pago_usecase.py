from users.domain.entities.detalle_pago import DetallePago

class CrearDetallePagoUseCase:
    def __init__(self, detalle_pago_repository):
        self.detalle_pago_repository = detalle_pago_repository

    def execute(self, pago_id, monto, descripcion=None):
        if monto <= 0:
            raise ValueError('El monto debe ser mayor que 0')

        detalle = DetallePago(pago_id=pago_id, monto=monto, descripcion=descripcion)
        return self.detalle_pago_repository.create(detalle)


class ListarDetallesPagoUseCase:
    def __init__(self, detalle_pago_repository):
        self.detalle_pago_repository = detalle_pago_repository

    def execute(self, pago_id=None):
        if pago_id is None:
            return self.detalle_pago_repository.get_all()
        return self.detalle_pago_repository.get_by_pago(pago_id)


class ActualizarDetallePagoUseCase:
    def __init__(self, detalle_pago_repository):
        self.detalle_pago_repository = detalle_pago_repository

    def execute(self, detalle_id, monto=None, descripcion=None):
        detalle = self.detalle_pago_repository.get_by_id(detalle_id)
        if not detalle:
            raise LookupError('Detalle de pago no encontrado')

        if monto is not None and monto <= 0:
            raise ValueError('El monto debe ser mayor que 0')

        detalle.monto = monto if monto is not None else detalle.monto
        detalle.descripcion = descripcion if descripcion is not None else detalle.descripcion

        return self.detalle_pago_repository.update(detalle)


class EliminarDetallePagoUseCase:
    def __init__(self, detalle_pago_repository):
        self.detalle_pago_repository = detalle_pago_repository

    def execute(self, detalle_id):
        if not self.detalle_pago_repository.delete(detalle_id):
            raise LookupError('No se pudo eliminar detalle de pago')
        return True
