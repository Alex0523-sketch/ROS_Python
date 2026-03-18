from django.db import models

class InventarioModel(models.Model):
    # Relación ManyToOne con Producto
    producto = models.ForeignKey(
        'ProductoModel', 
        on_delete=models.CASCADE, 
        db_column='producto_id',
        related_name='inventarios'
    )
    
    cantidad_disponible = models.IntegerField(null=False)
    cantidad_minima = models.IntegerField(null=False)
    
    # Timestamps de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventarios'
        app_label = 'users'

    def __str__(self):
        return f"Inventario de {self.producto.nombre}: {self.cantidad_disponible}"