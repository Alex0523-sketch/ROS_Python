from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Reserva:
    codigo_reserva: str
    mesa_id: int
    fecha_reserva: datetime
    hora: str
    numero_personas: int
    estado: str
    id: Optional[int] = None
    user_id: Optional[int] = None
    nombre_cliente: Optional[str] = None
    email_cliente: Optional[str] = None
    telefono_cliente: Optional[str] = None
    comentarios: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None