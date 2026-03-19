from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from ..entities.promocion import Promocion


class PromocionRepository(ABC):
    """Interfaz del repositorio de promociones"""
    
    @abstractmethod
    def get_by_id(self, promocion_id: int) -> Optional[Promocion]:
        """Obtiene una promoción por su ID"""
        pass
    
    @abstractmethod
    def get_activas(self) -> List[Promocion]:
        """Obtiene promociones activas"""
        pass
    
    @abstractmethod
    def get_vigentes(self) -> List[Promocion]:
        """Obtiene promociones vigentes (activas y dentro del rango de fechas)"""
        pass
    
    @abstractmethod
    def get_by_fecha(self, fecha: datetime) -> List[Promocion]:
        """Obtiene promociones vigentes en una fecha específica"""
        pass
    
    @abstractmethod
    def get_by_producto(self, producto_id: int) -> List[Promocion]:
        """Obtiene promociones que incluyen un producto específico"""
        pass
    
    @abstractmethod
    def get_proximas(self, dias: int = 7) -> List[Promocion]:
        """Obtiene promociones que comenzarán en los próximos días"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Promocion]:
        """Obtiene todas las promociones"""
        pass
    
    @abstractmethod
    def save(self, promocion: Promocion) -> Promocion:
        """Guarda una promoción"""
        pass
    
    @abstractmethod
    def update(self, promocion: Promocion) -> Promocion:
        """Actualiza una promoción"""
        pass
    
    @abstractmethod
    def delete(self, promocion_id: int) -> bool:
        """Elimina una promoción"""
        pass
