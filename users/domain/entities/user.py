from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserEntity:
    """Entidad de dominio. `password` solo en texto plano al crear/actualizar; en lectura suele ir vacío."""

    nombre: str
    apellido: str
    email: str
    activo: bool = True
    id_user: Optional[int] = None
    password: Optional[str] = None
    rol_id: Optional[int] = None
    is_staff: bool = False
    is_superuser: bool = False
    fecha_creacion: Optional[datetime] = None

    @property
    def pk(self) -> Optional[int]:
        """Alias del PK de Django (`id_user`)."""
        return self.id_user