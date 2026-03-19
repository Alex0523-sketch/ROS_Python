from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.horario import Horario


class HorarioRepository(ABC):
    """Interfaz del repositorio de horarios"""
    
    @abstractmethod
    def get_by_id(self, horario_id: int) -> Optional[Horario]:
        """Obtiene un horario por su ID"""
        pass
    
    @abstractmethod
    def get_by_dia(self, diaSemana: str) -> Optional[Horario]:
        """Obtiene el horario de un día específico"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, usuario_id: UUID) -> List[Horario]:
        """Obtiene los horarios de un usuario específico"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Horario]:
        """Obtiene todos los horarios"""
        pass
    
    @abstractmethod
    def save(self, horario: Horario) -> Horario:
        """Guarda un horario"""
        pass
    
    @abstractmethod
    def update(self, horario: Horario) -> Horario:
        """Actualiza un horario"""
        pass
    
    @abstractmethod
    def delete(self, horario_id: int) -> bool:
        """Elimina un horario"""
        pass
