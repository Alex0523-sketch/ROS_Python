from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

@dataclass
class Noticia:
    titulo: str
    contenido: str
    id: Optional[int] = None
    imagen: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    # Valor por defecto equivalente a = new Date()
    fecha_actualizacion: datetime = field(default_factory=datetime.now)