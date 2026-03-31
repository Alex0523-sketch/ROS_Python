<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.inventario import Inventario


class InventarioRepository(ABC):
    """Contrato alineado con `InventarioRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Inventario]:
        pass

    @abstractmethod
    def get_by_id(self, inventario_id: int) -> Optional[Inventario]:
        pass

    @abstractmethod
    def get_by_producto(self, producto_id: int) -> List[Inventario]:
        pass

    @abstractmethod
    def create(self, inventario: Inventario) -> Inventario:
        pass

    @abstractmethod
    def update(self, inventario_id: int, inventario: Inventario) -> Inventario:
        pass

    @abstractmethod
    def delete(self, inventario_id: int) -> bool:
        pass
=======
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.inventario import Inventario


class InventarioRepository(ABC):
    """Contrato alineado con `InventarioRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Inventario]:
        pass

    @abstractmethod
    def get_by_id(self, inventario_id: int) -> Optional[Inventario]:
        pass

    @abstractmethod
    def get_by_producto(self, producto_id: int) -> List[Inventario]:
        pass

    @abstractmethod
    def create(self, inventario: Inventario) -> Inventario:
        pass

    @abstractmethod
    def update(self, inventario_id: int, inventario: Inventario) -> Inventario:
        pass

    @abstractmethod
    def delete(self, inventario_id: int) -> bool:
        pass
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
