from django.db import models


class InsumoModel(models.Model):
    UNIDAD_CHOICES = [('g', 'Gramos'), ('ml', 'Mililitros')]

    nombre = models.CharField(max_length=100, unique=True)
    unidad = models.CharField(max_length=5, choices=UNIDAD_CHOICES, default='g')
    stock_actual = models.FloatField(default=0.0)
    stock_minimo = models.FloatField(default=0.0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'insumos'
        app_label = 'users'

    def __str__(self):
        return f'{self.nombre} ({self.stock_actual}{self.unidad})'

    @property
    def necesita_reposicion(self):
        return self.stock_actual <= self.stock_minimo
