<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.mesa import Mesa


class MesaRepository(ABC):
    """Contrato alineado con `MesaRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Mesa]:
        pass

    @abstractmethod
    def get_by_id(self, mesa_id: int) -> Optional[Mesa]:
        pass

    @abstractmethod
    def get_by_estado(self, estado: str) -> List[Mesa]:
        pass

    @abstractmethod
    def create(self, mesa: Mesa) -> Mesa:
        pass

    @abstractmethod
    def update(self, mesa_id: int, mesa: Mesa) -> Mesa:
        pass

    @abstractmethod
    def delete(self, mesa_id: int) -> bool:
        pass
=======
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.mesa import Mesa


class MesaRepository(ABC):
    """Contrato alineado con `MesaRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Mesa]:
        pass

    @abstractmethod
    def get_by_id(self, mesa_id: int) -> Optional[Mesa]:
        pass

    @abstractmethod
    def get_by_estado(self, estado: str) -> List[Mesa]:
        pass

    @abstractmethod
    def create(self, mesa: Mesa) -> Mesa:
        pass

    @abstractmethod
    def update(self, mesa_id: int, mesa: Mesa) -> Mesa:
        pass

    @abstractmethod
    def delete(self, mesa_id: int) -> bool:
        pass
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
