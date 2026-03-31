from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DetallePago:
    pago_id: int
    monto: float
    id: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None