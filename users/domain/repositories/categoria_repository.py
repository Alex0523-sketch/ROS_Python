from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.categoria import Categoria, EstadoCategoria


class CategoriaRepository(ABC):
    """Interfaz del repositorio de categorías"""
    
    @abstractmethod
    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        """Obtiene una categoría por su ID"""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        """Obtiene una categoría por su nombre"""
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: EstadoCategoria) -> List[Categoria]:
        """Obtiene categorías por su estado"""
        pass
    
    @abstractmethod
    def get_activas(self) -> List[Categoria]:
        """Obtiene categorías activas"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Categoria]:
        """Obtiene todas las categorías"""
        pass
    
    @abstractmethod
    def save(self, categoria: Categoria) -> Categoria:
        """Guarda una categoría"""
        pass
    
    @abstractmethod
    def update(self, categoria: Categoria) -> Categoria:
        """Actualiza una categoría"""
        pass
    
    @abstractmethod
    def delete(self, categoria_id: int) -> bool:
        """Elimina una categoría"""
        pass
