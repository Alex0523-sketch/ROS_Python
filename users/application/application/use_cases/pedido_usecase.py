from datetime import datetime
from uuid import uuid4
from users.domain.entities.pedido import Pedido


class CrearPedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_data: dict):
        if pedido_data.get("total", 0) <= 0:
            raise ValueError("El total del pedido debe ser mayor a 0.")

        if not pedido_data.get("cliente_nombre"):
            raise ValueError("El nombre del cliente es obligatorio.")

        if not pedido_data.get("estado"):
            pedido_data["estado"] = "PENDIENTE"

        if not pedido_data.get("codigo"):
            pedido_data["codigo"] = f"PED-{uuid4().hex[:8].upper()}"

        pedido = Pedido(
            total=pedido_data["total"],
            estado=pedido_data["estado"],
            user_id=pedido_data.get("user_id"),
            cliente_nombre=pedido_data.get("cliente_nombre"),
            numero_mesa=pedido_data.get("numero_mesa"),
            reserva_id=pedido_data.get("reserva_id"),
            empleado_id=pedido_data.get("empleado_id"),
            comentarios=pedido_data.get("comentarios"),
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
        )

        if hasattr(self.pedido_repository, "create"):
            return self.pedido_repository.create(pedido)

        return self.pedido_repository.save(pedido)


class ObtenerPedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id: int):
        pedido = self.pedido_repository.get_by_id(pedido_id)
        if not pedido:
            raise LookupError("Pedido no encontrado")
        return pedido


class ListarPedidosUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self):
        return self.pedido_repository.get_all()


class ActualizarPedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id: int, pedido_data: dict):
        pedido_existente = self.pedido_repository.get_by_id(pedido_id)
        if not pedido_existente:
            raise LookupError("Pedido no existe")

        pedido_actualizado = Pedido(
            id=pedido_existente.id,
            total=pedido_data.get("total", pedido_existente.total),
            estado=pedido_data.get("estado", pedido_existente.estado),
            user_id=pedido_data.get("user_id", pedido_existente.user_id),
            cliente_nombre=pedido_data.get("cliente_nombre", pedido_existente.cliente_nombre),
            numero_mesa=pedido_data.get("numero_mesa", pedido_existente.numero_mesa),
            reserva_id=pedido_data.get("reserva_id", pedido_existente.reserva_id),
            empleado_id=pedido_data.get("empleado_id", pedido_existente.empleado_id),
            comentarios=pedido_data.get("comentarios", pedido_existente.comentarios),
            fecha_creacion=pedido_existente.fecha_creacion,
            fecha_actualizacion=datetime.now(),
        )

        if hasattr(self.pedido_repository, "update"):
            try:
                return self.pedido_repository.update(pedido_id, pedido_actualizado)
            except TypeError:
                return self.pedido_repository.update(pedido_actualizado)

        raise AttributeError("Repositorio no soporta actualización de pedido")


class EliminarPedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id: int):
        eliminado = self.pedido_repository.delete(pedido_id)
        if not eliminado:
            raise LookupError("No se pudo eliminar el pedido (no existe).")
        return True


class CambiarEstadoPedidoUseCase:
    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository

    def execute(self, pedido_id: int, nuevo_estado: str):
        pedido = self.pedido_repository.get_by_id(pedido_id)
        if not pedido:
            raise LookupError("Pedido no encontrado")

        if pedido.estado == "CANCELADO" and nuevo_estado != "CANCELADO":
            raise ValueError("No se puede cambiar el estado de un pedido cancelado")

        pedido.estado = nuevo_estado
        pedido.fecha_actualizacion = datetime.now()

        if hasattr(self.pedido_repository, "cambiar_estado"):
            return self.pedido_repository.cambiar_estado(pedido_id, nuevo_estado)

        return self.pedido_repository.update(pedido_id, pedido)
