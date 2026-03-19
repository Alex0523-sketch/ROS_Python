from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ..entities.pago import Pago, EstadoPago, MetodoPago


class PagoRepository(ABC):
    """Interfaz del repositorio de pagos"""
    
    @abstractmethod
    def get_by_id(self, pago_id: int) -> Optional[Pago]:
        """Obtiene un pago por su ID"""
        pass
    
    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Pago]:
        """Obtiene un pago por su código de transacción"""
        pass
    
    @abstractmethod
    def get_by_pedido(self, pedido_id: int) -> Optional[Pago]:
        """Obtiene el pago de un pedido"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, usuario_id: UUID) -> List[Pago]:
        """Obtiene pagos de un usuario"""
        pass
    
    @abstractmethod
    def get_by_estado(self, estado: EstadoPago) -> List[Pago]:
        """Obtiene pagos por estado"""
        pass
    
    @abstractmethod
    def get_by_metodo(self, metodo: MetodoPago) -> List[Pago]:
        """Obtiene pagos por método"""
        pass
    
    @abstractmethod
    def get_by_fecha(self, fecha: datetime) -> List[Pago]:
        """Obtiene pagos de una fecha"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Pago]:
        """Obtiene todos los pagos"""
        pass
    
    @abstractmethod
    def save(self, pago: Pago) -> Pago:
        """Guarda un pago"""
        pass
    
    @abstractmethod
    def update(self, pago: Pago) -> Pago:
        """Actualiza un pago"""
        pass
    
    @abstractmethod
    def delete(self, pago_id: int) -> bool:
        """Elimina un pago"""
        pass
    
    @abstractmethod
    def procesar_pago(self, pago: Pago) -> Pago:
        """Procesa un pago"""
        pass
    
    @abstractmethod
    def confirmar_pago(self, pago_id: int) -> Optional[Pago]:
        """Confirma un pago"""
        pass
    
    @abstractmethod
    def rechazar_pago(self, pago_id: int) -> Optional[Pago]:
        """Rechaza un pago"""
        pass
