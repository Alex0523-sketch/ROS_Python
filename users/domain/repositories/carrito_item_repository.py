from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.carrito_item import CarritoItem


class CarritoItemRepository(ABC):
    """Interfaz del repositorio de items del carrito"""
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[CarritoItem]:
        """Obtiene un item por su ID"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, usuario_id: UUID) -> List[CarritoItem]:
        """Obtiene los items del carrito de un usuario"""
        pass
    
    @abstractmethod
    def get_by_producto(self, usuario_id: UUID, producto_id: int) -> Optional[CarritoItem]:
        """Obtiene un item específico del carrito de un usuario"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[CarritoItem]:
        """Obtiene todos los items"""
        pass
    
    @abstractmethod
    def save(self, item: CarritoItem) -> CarritoItem:
        """Guarda un item en el carrito"""
        pass
    
    @abstractmethod
    def update(self, item: CarritoItem) -> CarritoItem:
        """Actualiza un item del carrito"""
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Elimina un item del carrito"""
        pass
    
    @abstractmethod
    def delete_by_usuario(self, usuario_id: UUID) -> bool:
        """Vacía el carrito de un usuario"""
        pass
    
    @abstractmethod
    def contar_items(self, usuario_id: UUID) -> int:
        """Cuenta los items en el carrito de un usuario"""
        pass
    
    @abstractmethod
    def calcular_total(self, usuario_id: UUID) -> float:
        """Calcula el total del carrito de un usuario"""
        pass
