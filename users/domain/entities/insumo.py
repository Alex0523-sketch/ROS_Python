from dataclasses import dataclass
from typing import Optional


@dataclass
class Insumo:
    nombre: str
    unidad: str
    stock_actual: float
    stock_minimo: float
    id: Optional[int] = None

    @property
    def necesita_reposicion(self) -> bool:
        return self.stock_actual <= self.stock_minimo


@dataclass
class RecetaItem:
    producto_id: int
    insumo_id: int
    cantidad: float
    id: Optional[int] = None
    insumo_nombre: Optional[str] = None
    insumo_unidad: Optional[str] = None
