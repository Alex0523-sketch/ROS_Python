from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List

@dataclass
class Promocion:
    titulo: str
    descuento: float
    fecha_inicio: date
    fecha_fin: date
    id_promocion: Optional[int] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    productos: List[int] = field(default_factory=list) # IDs de productos vinculados
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None