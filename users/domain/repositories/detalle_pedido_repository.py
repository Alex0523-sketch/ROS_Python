from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.detalle_pedido import DetallePedido


class DetallePedidoRepository(ABC):
    """Interfaz del repositorio de detalles de pedido"""
    
    @abstractmethod
    def get_by_id(self, detalle_id: int) -> Optional[DetallePedido]:
        """Obtiene un detalle por su ID"""
        pass
    
    @abstractmethod
    def get_by_pedido(self, pedido_id: int) -> List[DetallePedido]:
        """Obtiene los detalles de un pedido"""
        pass
    
    @abstractmethod
    def get_by_producto(self, producto_id: int) -> List[DetallePedido]:
        """Obtiene detalles por producto"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[DetallePedido]:
        """Obtiene todos los detalles"""
        pass
    
    @abstractmethod
    def save(self, detalle: DetallePedido) -> DetallePedido:
        """Guarda un detalle"""
        pass
    
    @abstractmethod
    def save_multiples(self, detalles: List[DetallePedido]) -> List[DetallePedido]:
        """Guarda múltiples detalles"""
        pass
    
    @abstractmethod
    def update(self, detalle: DetallePedido) -> DetallePedido:
        """Actualiza un detalle"""
        pass
    
    @abstractmethod
    def delete(self, detalle_id: int) -> bool:
        """Elimina un detalle"""
        pass
    
    @abstractmethod
    def delete_by_pedido(self, pedido_id: int) -> bool:
        """Elimina todos los detalles de un pedido"""
        pass
    
    @abstractmethod
    def calcular_subtotal(self, pedido_id: int) -> float:
        """Calcula el subtotal de un pedido"""
        pass
