from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from ..entities.pedido import Pedido, EstadoPedido


class PedidoRepository(ABC):
    """Interfaz del repositorio de pedidos"""
    
    @abstractmethod
    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        """Obtiene un pedido por su ID"""
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Pedido]:
        """Obtiene un pedido por su código único"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, usuario_id: UUID) -> List[Pedido]:
        """Obtiene pedidos de un usuario"""
        pass
    
    @abstractmethod
    def get_by_mesa(self, mesa_id: int) -> List[Pedido]:
        """Obtiene pedidos de una mesa"""
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: EstadoPedido) -> List[Pedido]:
        """Obtiene pedidos por estado"""
        pass
    
    @abstractmethod
    def get_by_fecha(self, fecha: datetime) -> List[Pedido]:
        """Obtiene pedidos de una fecha específica"""
        pass
    
    @abstractmethod
    def get_pendientes(self) -> List[Pedido]:
        """Obtiene pedidos pendientes"""
        pass
    
    @abstractmethod
    def get_en_preparacion(self) -> List[Pedido]:
        """Obtiene pedidos en preparación"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Pedido]:
        """Obtiene todos los pedidos"""
        pass
    
    @abstractmethod
    def save(self, pedido: Pedido) -> Pedido:
        """Guarda un pedido"""
        pass
    
    @abstractmethod
    def update(self, pedido: Pedido) -> Pedido:
        """Actualiza un pedido"""
        pass
    
    @abstractmethod
    def delete(self, pedido_id: int) -> bool:
        """Elimina un pedido"""
        pass
    
    @abstractmethod
    def cambiar_estado(self, pedido_id: int, nuevo_estado: EstadoPedido) -> Optional[Pedido]:
        """Cambia el estado de un pedido"""
        pass
