from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.producto import Producto


class ProductoRepository(ABC):
    """Contrato alineado con `ProductoRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Producto]:
        pass

    @abstractmethod
    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def get_by_categoria(self, categoria_id: int) -> List[Producto]:
        pass

    @abstractmethod
    def create(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def update(self, producto_id: int, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def delete(self, producto_id: int) -> bool:
        pass
