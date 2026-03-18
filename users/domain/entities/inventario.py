from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Inventario:
    producto_id: int
    cantidad_disponible: int
    cantidad_minima: int
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    def necesita_reabastecimiento(self) -> bool:
        return self.cantidad_disponible <= self.cantidad_minima