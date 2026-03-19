from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from ..entities.noticia import Noticia


class NoticiaRepository(ABC):
    """Interfaz del repositorio de noticias"""
    
    @abstractmethod
    def get_by_id(self, noticia_id: int) -> Optional[Noticia]:
        """Obtiene una noticia por su ID"""
        pass
    
    @abstractmethod
    def get_recientes(self, limite: int = 10) -> List[Noticia]:
        """Obtiene las noticias más recientes"""
        pass
    
    @abstractmethod
    def get_destacadas(self) -> List[Noticia]:
        """Obtiene noticias destacadas"""
        pass
    
    @abstractmethod
    def get_by_fecha(self, fecha: datetime) -> List[Noticia]:
        """Obtiene noticias de una fecha específica"""
        pass
    
    @abstractmethod
    def get_by_rango_fechas(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Noticia]:
        """Obtiene noticias en un rango de fechas"""
        pass
    
    @abstractmethod
    def buscar_por_titulo(self, texto: str) -> List[Noticia]:
        """Busca noticias por título (búsqueda parcial)"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Noticia]:
        """Obtiene todas las noticias"""
        pass
    
    @abstractmethod
    def save(self, noticia: Noticia) -> Noticia:
        """Guarda una noticia"""
        pass
    
    @abstractmethod
    def update(self, noticia: Noticia) -> Noticia:
        """Actualiza una noticia"""
        pass
    
    @abstractmethod
    def delete(self, noticia_id: int) -> bool:
        """Elimina una noticia"""
        pass
