from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserEntity:
    id_user: Optional[int]
    nombre: str
    apellido: str
    email: str
    password: str
    activo: bool
    rol_id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None