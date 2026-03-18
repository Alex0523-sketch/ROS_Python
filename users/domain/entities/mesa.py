from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Mesa:
    numero_mesa: int
    capacidad: int
    estado: str # "libre", "ocupada", "reservada"
    id_mesa: Optional[int] = None
    ubicacion: Optional[str] = None
    fecha_creacion: Optional[datetime] = None