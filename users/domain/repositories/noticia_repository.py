<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.noticia import Noticia


class NoticiaRepository(ABC):
    """Contrato alineado con `NoticiaRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Noticia]:
        pass

    @abstractmethod
    def get_by_id(self, noticia_id: int) -> Optional[Noticia]:
        pass

    @abstractmethod
    def create(self, noticia: Noticia) -> Noticia:
        pass

    @abstractmethod
    def update(self, noticia_id: int, noticia: Noticia) -> Noticia:
        pass

    @abstractmethod
    def delete(self, noticia_id: int) -> bool:
        pass
=======
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.noticia import Noticia


class NoticiaRepository(ABC):
    """Contrato alineado con `NoticiaRepositoryImpl`."""

    @abstractmethod
    def get_all(self) -> List[Noticia]:
        pass

    @abstractmethod
    def get_by_id(self, noticia_id: int) -> Optional[Noticia]:
        pass

    @abstractmethod
    def create(self, noticia: Noticia) -> Noticia:
        pass

    @abstractmethod
    def update(self, noticia_id: int, noticia: Noticia) -> Noticia:
        pass

    @abstractmethod
    def delete(self, noticia_id: int) -> bool:
        pass
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
