from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.carrito_item import CarritoItem


class CarritoItemRepository(ABC):
    """Contrato alineado con `CarritoItemRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[CarritoItem]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[CarritoItem]:
        pass

    @abstractmethod
    def create(self, item: CarritoItem) -> CarritoItem:
        pass

    @abstractmethod
    def update(self, item_id: int, item: CarritoItem) -> CarritoItem:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass
