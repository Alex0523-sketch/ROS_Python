from django.db import models

class DetallePedidoModel(models.Model):
    # on_delete=models.CASCADE: Si borras el Pedido, se borran sus detalles.
    pedido = models.ForeignKey(
        'PedidoModel', 
        on_delete=models.CASCADE, 
        db_column='pedido_id',
        related_name='detalles' # Esto permite hacer pedido.detalles.all()
    )
    
    # on_delete=models.PROTECT: No permite borrar un Producto si está en un pedido.
    producto = models.ForeignKey(
        'ProductoModel', 
        on_delete=models.PROTECT, 
        db_column='producto_id'
    )
    
    cantidad = models.IntegerField(null=False)
    
    # Mantenemos FloatField por fidelidad a tu código Java (Double)
    precio = models.FloatField(null=False)

    class Meta:
        db_table = 'detalle_pedidos'
        app_label = 'users'

    @property
    def subtotal_linea(self):
        return float(self.precio) * int(self.cantidad)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Pedido {self.pedido.id})"