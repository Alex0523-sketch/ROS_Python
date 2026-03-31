from dataclasses import dataclass
from typing import Optional

@dataclass
class DetallePedido:
    pedido_id: int
    producto_id: int
    cantidad: int
    precio: float
    id: Optional[int] = None

    def calcular_subtotal(self) -> float:
        return self.cantidad * self.precio