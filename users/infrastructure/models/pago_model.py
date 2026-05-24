from django.db import models

class PagoModel(models.Model):
    # Relación opcional con el usuario que realiza el pago
    user = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='user_id'
    )
    
    # Relación obligatoria con el Pedido
    pedido = models.ForeignKey(
        'PedidoModel', 
        on_delete=models.CASCADE, 
        db_column='pedido_id',
        related_name='pagos'
    )
    
    metodo_pago = models.CharField(max_length=50)
    monto_total = models.FloatField()
    estado = models.CharField(max_length=50)  # PENDIENTE, COMPLETADO, RECHAZADO
    email_cliente = models.EmailField(max_length=150, null=True, blank=True)
    motivo_rechazo = models.TextField(max_length=500, null=True, blank=True)

    fecha_pago = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pagos'
        app_label = 'users'

    def __str__(self):
        return f"Pago {self.id} - {self.metodo_pago} - {self.monto_total}"