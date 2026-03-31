from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.promocion import Promocion


class PromocionRepository(ABC):
    """Contrato alineado con `PromocionRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Promocion]:
        pass

    @abstractmethod
    def get_by_id(self, promocion_id: int) -> Optional[Promocion]:
        pass

    @abstractmethod
    def create(self, promocion: Promocion) -> Promocion:
        pass

    @abstractmethod
    def update(self, promocion_id: int, promocion: Promocion) -> Promocion:
        pass

    @abstractmethod
    def delete(self, promocion_id: int) -> bool:
        pass
