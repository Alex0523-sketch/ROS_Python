from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.inventario import Inventario


class InventarioRepository(ABC):
    """Interfaz del repositorio de inventario"""
    
    @abstractmethod
    def get_by_id(self, inventario_id: int) -> Optional[Inventario]:
        """Obtiene un registro de inventario por su ID"""
        pass
    
    @abstractmethod
    def get_by_producto(self, producto_id: int) -> Optional[Inventario]:
        """Obtiene el inventario de un producto específico"""
        pass
    
    @abstractmethod
    def get_bajo_stock(self) -> List[Inventario]:
        """Obtiene productos con stock menor al mínimo"""
        pass
    
    @abstractmethod
    def get_agotados(self) -> List[Inventario]:
        """Obtiene productos agotados (cantidad = 0)"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Inventario]:
        """Obtiene todos los registros de inventario"""
        pass
    
    @abstractmethod
    def save(self, inventario: Inventario) -> Inventario:
        """Guarda un registro de inventario"""
        pass
    
    @abstractmethod
    def update(self, inventario: Inventario) -> Inventario:
        """Actualiza un registro de inventario"""
        pass
    
    @abstractmethod
    def delete(self, inventario_id: int) -> bool:
        """Elimina un registro de inventario"""
        pass
    
    @abstractmethod
    def ajustar_stock(self, producto_id: int, cantidad: int) -> Optional[Inventario]:
        """Ajusta el stock de un producto (suma o resta)"""
        pass
