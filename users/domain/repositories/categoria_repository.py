from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.categoria import Categoria


class CategoriaRepository(ABC):
    """Contrato alineado con `CategoriaRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Categoria]:
        pass

    @abstractmethod
    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        pass

    @abstractmethod
    def create(self, categoria: Categoria) -> Categoria:
        pass

    @abstractmethod
    def update(self, categoria_id: int, categoria: Categoria) -> Categoria:
        pass

    @abstractmethod
    def delete(self, categoria_id: int) -> bool:
        pass
