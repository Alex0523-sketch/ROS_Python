from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.rol import Rol


class RolRepository(ABC):
    """Interfaz del repositorio de roles"""
    
    @abstractmethod
    def get_by_id(self, rol_id: int) -> Optional[Rol]:
        """Obtiene un rol por su ID"""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        """Obtiene un rol por su nombre"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, usuario_id: UUID) -> List[Rol]:
        """Obtiene los roles de un usuario"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Rol]:
        """Obtiene todos los roles"""
        pass
    
    @abstractmethod
    def save(self, rol: Rol) -> Rol:
        """Guarda un rol"""
        pass
    
    @abstractmethod
    def update(self, rol: Rol) -> Rol:
        """Actualiza un rol"""
        pass
    
    @abstractmethod
    def delete(self, rol_id: int) -> bool:
        """Elimina un rol"""
        pass
    
    @abstractmethod
    def asignar_a_usuario(self, usuario_id: UUID, rol_id: int) -> bool:
        """Asigna un rol a un usuario"""
        pass
    
    @abstractmethod
    def quitar_de_usuario(self, usuario_id: UUID, rol_id: int) -> bool:
        """Quita un rol de un usuario"""
        pass
