from dataclasses import dataclass
from typing import Optional

@dataclass
class CarritoItem:
    producto_id: int
    nombre: str
    precio: float
    cantidad: int
    subtotal: float = 0.0

    def __post_init__(self):
        """
        Equivalente al cuerpo del constructor en Java.
        Se ejecuta automáticamente después de crear la instancia.
        """
        self.calcular_subtotal()

    def calcular_subtotal(self):
        self.subtotal = self.precio * self.cantidad