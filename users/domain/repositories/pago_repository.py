<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.pago import Pago


class PagoRepository(ABC):
    """Contrato alineado con `PagoRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Pago]:
        pass

    @abstractmethod
    def get_by_id(self, pago_id: int) -> Optional[Pago]:
        pass

    @abstractmethod
    def get_by_pedido(self, pedido_id: int) -> List[Pago]:
        pass

    @abstractmethod
    def create(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def update(self, pago_id: int, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def delete(self, pago_id: int) -> bool:
        pass
=======
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.pago import Pago


class PagoRepository(ABC):
    """Contrato alineado con `PagoRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Pago]:
        pass

    @abstractmethod
    def get_by_id(self, pago_id: int) -> Optional[Pago]:
        pass

    @abstractmethod
    def get_by_pedido(self, pedido_id: int) -> List[Pago]:
        pass

    @abstractmethod
    def create(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def update(self, pago_id: int, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def delete(self, pago_id: int) -> bool:
        pass
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
