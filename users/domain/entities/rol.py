from dataclasses import dataclass
from typing import Optional

@dataclass
class Rol:
    nombre: str
    id_rol: Optional[int] = None