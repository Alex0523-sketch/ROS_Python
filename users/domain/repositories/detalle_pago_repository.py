from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.detalle_pago import DetallePago


class DetallePagoRepository(ABC):
    """Contrato alineado con `DetallePagoRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[DetallePago]:
        pass

    @abstractmethod
    def get_by_id(self, detalle_id: int) -> Optional[DetallePago]:
        pass

    @abstractmethod
    def get_by_pago(self, pago_id: int) -> List[DetallePago]:
        pass

    @abstractmethod
    def create(self, detalle: DetallePago) -> DetallePago:
        pass

    @abstractmethod
    def update(self, detalle_id: int, detalle: DetallePago) -> DetallePago:
        pass

    @abstractmethod
    def delete(self, detalle_id: int) -> bool:
        pass
