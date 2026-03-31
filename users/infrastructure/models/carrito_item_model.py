from django.db import models

class CarritoItemModel(models.Model):
    # Relación con el producto real
    producto = models.ForeignKey(
        'ProductoModel', 
        on_delete=models.CASCADE,
        db_column='id_producto'
    )
    
    # Guardamos nombre y precio por si el producto cambia en el futuro (histórico)
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    cantidad = models.IntegerField(default=1)
    subtotal = models.FloatField()

    class Meta:
        db_table = 'carrito_items'
        app_label = 'users'

    def save(self, *args, **kwargs):
        # Aseguramos que el subtotal se calcule antes de guardar en la DB
        self.subtotal = self.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.nombre}"