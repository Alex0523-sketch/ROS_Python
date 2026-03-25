from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.rol import Rol


class RolRepository(ABC):
    """Contrato alineado con `RolRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Rol]:
        pass

    @abstractmethod
    def get_by_id(self, rol_id: int) -> Optional[Rol]:
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        pass

    @abstractmethod
    def create(self, rol: Rol) -> Rol:
        pass

    @abstractmethod
    def update(self, rol_id: int, rol: Rol) -> Rol:
        pass

    @abstractmethod
    def delete(self, rol_id: int) -> bool:
        pass
