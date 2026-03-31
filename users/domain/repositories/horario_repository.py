from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.horario import Horario


class HorarioRepository(ABC):
    """Contrato alineado con `HorarioRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Horario]:
        pass

    @abstractmethod
    def get_by_id(self, horario_id: int) -> Optional[Horario]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Horario]:
        pass

    @abstractmethod
    def create(self, horario: Horario) -> Horario:
        pass

    @abstractmethod
    def update(self, horario_id: int, horario: Horario) -> Horario:
        pass

    @abstractmethod
    def delete(self, horario_id: int) -> bool:
        pass
