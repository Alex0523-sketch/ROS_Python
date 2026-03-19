from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date
from uuid import UUID

from ..entities.reserva import Reserva, EstadoReserva


class ReservaRepository(ABC):
    """Interfaz del repositorio de reservas"""
    
    @abstractmethod
    def get_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """Obtiene una reserva por su ID"""
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: int) -> Optional[Reserva]:
        """Obtiene una reserva por su código único"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, usuario_id: UUID) -> List[Reserva]:
        """Obtiene reservas de un usuario específico"""
        pass
    
    @abstractmethod
    def get_by_fecha(self, fecha: date) -> List[Reserva]:
        """Obtiene reservas de una fecha específica"""
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: EstadoReserva) -> List[Reserva]:
        """Obtiene reservas por su estado"""
        pass
    
    @abstractmethod
    def get_by_mesa(self, mesa_id: int, fecha: date) -> List[Reserva]:
        """Obtiene reservas de una mesa en una fecha específica"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Reserva]:
        """Obtiene todas las reservas"""
        pass
    
    @abstractmethod
    def save(self, reserva: Reserva) -> Reserva:
        """Guarda una reserva"""
        pass
    
    @abstractmethod
    def update(self, reserva: Reserva) -> Reserva:
        """Actualiza una reserva"""
        pass
    
    @abstractmethod
    def delete(self, reserva_id: int) -> bool:
        """Elimina una reserva"""
        pass
    
    @abstractmethod
    def confirmar(self, reserva_id: int) -> Optional[Reserva]:
        """Confirma una reserva"""
        pass
    
    @abstractmethod
    def cancelar(self, reserva_id: int) -> Optional[Reserva]:
        """Cancela una reserva"""
        pass
