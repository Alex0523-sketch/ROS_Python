from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Horario:
    user_id: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None