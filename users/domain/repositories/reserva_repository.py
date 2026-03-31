from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.reserva import Reserva


class ReservaRepository(ABC):
    """Contrato alineado con `ReservaRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Reserva]:
        pass

    @abstractmethod
    def get_by_id(self, reserva_id: int) -> Optional[Reserva]:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Reserva]:
        pass

    @abstractmethod
    def get_by_estado(self, estado: str) -> List[Reserva]:
        pass

    @abstractmethod
    def create(self, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def update(self, reserva_id: int, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def delete(self, reserva_id: int) -> bool:
        pass
