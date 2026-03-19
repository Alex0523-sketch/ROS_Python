from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.detalle_pago import DetallePago


class DetallePagoRepository(ABC):
    """Interfaz del repositorio de detalles de pago"""
    
    @abstractmethod
    def get_by_id(self, detalle_id: int) -> Optional[DetallePago]:
        """Obtiene un detalle por su ID"""
        pass
    
    @abstractmethod
    def get_by_pago(self, pago_id: int) -> List[DetallePago]:
        """Obtiene los detalles de un pago"""
        pass
    
    @abstractmethod
    def get_by_metodo(self, metodo: str) -> List[DetallePago]:
        """Obtiene detalles por método de pago"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[DetallePago]:
        """Obtiene todos los detalles"""
        pass
    
    @abstractmethod
    def save(self, detalle: DetallePago) -> DetallePago:
        """Guarda un detalle"""
        pass
    
    @abstractmethod
    def update(self, detalle: DetallePago) -> DetallePago:
        """Actualiza un detalle"""
        pass
    
    @abstractmethod
    def delete(self, detalle_id: int) -> bool:
        """Elimina un detalle"""
        pass
    
    @abstractmethod
    def delete_by_pago(self, pago_id: int) -> bool:
        """Elimina todos los detalles de un pago"""
        pass
