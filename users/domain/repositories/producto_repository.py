from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.producto import Producto, EstadoProducto, TipoProducto


class ProductoRepository(ABC):
    """Interfaz del repositorio de productos"""
    
    @abstractmethod
    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: int) -> Optional[Producto]:
        """Obtiene un producto por su código"""
        pass
    
    @abstractmethod
    def get_by_categoria(self, categoria_id: int) -> List[Producto]:
        """Obtiene productos por categoría"""
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo: TipoProducto) -> List[Producto]:
        """Obtiene productos por tipo"""
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: EstadoProducto) -> List[Producto]:
        """Obtiene productos por estado"""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> List[Producto]:
        """Obtiene productos que contengan el nombre (búsqueda parcial)"""
        pass
    
    @abstractmethod
    def get_destacados(self, limite: int = 10) -> List[Producto]:
        """Obtiene productos destacados"""
        pass
    
    @abstractmethod
    def get_en_oferta(self) -> List[Producto]:
        """Obtiene productos con descuento"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Producto]:
        """Obtiene todos los productos"""
        pass
    
    @abstractmethod
    def save(self, producto: Producto) -> Producto:
        """Guarda un producto"""
        pass
    
    @abstractmethod
    def update(self, producto: Producto) -> Producto:
        """Actualiza un producto"""
        pass
    
    @abstractmethod
    def delete(self, producto_id: int) -> bool:
        """Elimina un producto"""
        pass
    
    @abstractmethod
    def aplicar_descuento(self, producto_id: int, descuento: float) -> Optional[Producto]:
        """Aplica un descuento a un producto"""
        pass
