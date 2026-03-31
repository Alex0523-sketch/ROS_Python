from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.user import UserEntity


class UserRepository(ABC):
    """Contrato del repositorio de usuarios (implementación en infrastructure)."""

    @abstractmethod
    def get_all(self) -> List[UserEntity]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
<<<<<<< HEAD
    def update(self, user_id: int, user: UserEntity, *, new_password: Optional[str] = None) -> Optional[UserEntity]:
=======
    def update(self, user_id: int, user: UserEntity, *, new_password: str | None = None) -> Optional[UserEntity]:
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass
