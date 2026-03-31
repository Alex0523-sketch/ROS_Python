from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Producto:
    nombre: str
    precio: float
    categoria_id: int
    id_producto: Optional[int] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None