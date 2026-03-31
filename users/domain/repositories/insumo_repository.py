from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.insumo import Insumo, RecetaItem


class InsumoRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Insumo]:
        pass

    @abstractmethod
    def get_by_id(self, insumo_id: int) -> Optional[Insumo]:
        pass

    @abstractmethod
    def create(self, insumo: Insumo) -> Insumo:
        pass

    @abstractmethod
    def update_stock(self, insumo_id: int, nuevo_stock: float) -> None:
        pass

    @abstractmethod
    def get_bajo_minimo(self) -> List[Insumo]:
        pass


class RecetaRepository(ABC):

    @abstractmethod
    def get_by_producto(self, producto_id: int) -> List[RecetaItem]:
        pass

    @abstractmethod
    def create(self, item: RecetaItem) -> RecetaItem:
        pass

    @abstractmethod
    def delete_by_producto(self, producto_id: int) -> None:
        pass
