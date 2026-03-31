<<<<<<< HEAD
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
=======
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
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
