from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date

from ..entities.mesa import Mesa, EstadoMesa, UbicacionMesa


class MesaRepository(ABC):
    """Interfaz del repositorio de mesas"""
    
    @abstractmethod
    def get_by_id(self, mesa_id: int) -> Optional[Mesa]:
        """Obtiene una mesa por su ID"""
        pass
    
    @abstractmethod
    def get_by_numero(self, numero: int) -> Optional[Mesa]:
        """Obtiene una mesa por su número"""
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: EstadoMesa) -> List[Mesa]:
        """Obtiene mesas por su estado"""
        pass
    
    @abstractmethod
    def get_by_ubicacion(self, ubicacion: UbicacionMesa) -> List[Mesa]:
        """Obtiene mesas por su ubicación"""
        pass
    
    @abstractmethod
    def get_by_capacidad(self, capacidad: int, operador: str = 'gte') -> List[Mesa]:
        """Obtiene mesas por capacidad (gte: mayor o igual, lte: menor o igual, eq: igual)"""
        pass
    
    @abstractmethod
    def get_disponibles(self, fecha: date, hora: str, personas: int) -> List[Mesa]:
        """Obtiene mesas disponibles para una fecha, hora y número de personas"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Mesa]:
        """Obtiene todas las mesas"""
        pass
    
    @abstractmethod
    def save(self, mesa: Mesa) -> Mesa:
        """Guarda una mesa"""
        pass
    
    @abstractmethod
    def update(self, mesa: Mesa) -> Mesa:
        """Actualiza una mesa"""
        pass
    
    @abstractmethod
    def delete(self, mesa_id: int) -> bool:
        """Elimina una mesa"""
        pass
    
    @abstractmethod
    def contar_mesas_por_estado(self) -> dict:
        """Cuenta mesas por estado (disponible, ocupada, reservada, mantenimiento)"""
        pass
