from django.db import models


class RecetaItemModel(models.Model):
    producto = models.ForeignKey(
        'ProductoModel',
        on_delete=models.CASCADE,
        related_name='receta_items',
        db_column='producto_id',
    )
    insumo = models.ForeignKey(
        'InsumoModel',
        on_delete=models.PROTECT,
        related_name='receta_items',
        db_column='insumo_id',
    )
    cantidad = models.FloatField()  # en la unidad del insumo (g o ml)

    class Meta:
        db_table = 'receta_items'
        app_label = 'users'
        unique_together = ('producto', 'insumo')

    def __str__(self):
        return f'{self.producto.nombre} → {self.cantidad}{self.insumo.unidad} de {self.insumo.nombre}'
