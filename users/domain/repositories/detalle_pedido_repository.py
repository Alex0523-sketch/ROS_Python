from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.detalle_pedido import DetallePedido


class DetallePedidoRepository(ABC):
    """Contrato alineado con `DetallePedidoRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[DetallePedido]:
        pass

    @abstractmethod
    def get_by_id(self, detalle_id: int) -> Optional[DetallePedido]:
        pass

    @abstractmethod
    def get_by_pedido(self, pedido_id: int) -> List[DetallePedido]:
        pass

    @abstractmethod
    def create(self, detalle: DetallePedido) -> DetallePedido:
        pass

    @abstractmethod
    def update(self, detalle_id: int, detalle: DetallePedido) -> DetallePedido:
        pass

    @abstractmethod
    def delete(self, detalle_id: int) -> bool:
        pass
