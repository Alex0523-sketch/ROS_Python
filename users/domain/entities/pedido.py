from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Pedido:
    total: float
    estado: str
    id: Optional[int] = None
    user_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    numero_mesa: Optional[str] = None
    reserva_id: Optional[int] = None
    empleado_id: Optional[int] = None
    comentarios: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    # Lista de IDs o objetos de DetallePedido
    detalles: List = field(default_factory=list)