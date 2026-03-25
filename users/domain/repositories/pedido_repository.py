from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.pedido import Pedido


class PedidoRepository(ABC):
    """Contrato alineado con `PedidoRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Pedido]:
        pass

    @abstractmethod
    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        pass

    @abstractmethod
    def get_by_estado(self, estado: str) -> List[Pedido]:
        pass

    @abstractmethod
    def create(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def update(self, pedido_id: int, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def delete(self, pedido_id: int) -> bool:
        pass
