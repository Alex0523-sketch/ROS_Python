from django.db import models

class DetallePagoModel(models.Model):
    # Relación con el Pago principal
    pago = models.ForeignKey(
        'PagoModel', 
        on_delete=models.CASCADE, 
        db_column='pago_id',
        related_name='detalles'
    )
    
    monto = models.FloatField(null=False)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    
    # Auditoría automática
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'detalle_pagos'
        app_label = 'users'

    def __str__(self):
        return f"Detalle Pago {self.id}: {self.monto} ({self.descripcion})"