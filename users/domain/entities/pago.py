from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List

@dataclass
class Pago:
    metodo_pago: str
    monto_total: float
    estado: str
    pedido_id: int
    id: Optional[int] = None
    user_id: Optional[int] = None
    fecha_pago: Optional[date] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    # Lista de detalles del pago (ej: propinas, impuestos, etc.)
    detalles: List = field(default_factory=list)