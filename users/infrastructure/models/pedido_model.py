from django.db import models

class PedidoModel(models.Model):
<<<<<<< HEAD
=======
    # Cliente (puede ser nulo si es venta directa)
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
    user = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='cliente_id',
        related_name='pedidos_cliente'
    )
    
<<<<<<< HEAD
    codigo_pedido = models.CharField(max_length=20, unique=True, null=True, blank=True)
=======
>>>>>>> 8611a3375ca4fbda1576200cb6dbacd6df17f1f0
    cliente_nombre = models.CharField(max_length=100, null=True, blank=True)
    numero_mesa = models.CharField(max_length=10, null=True, blank=True)
    
    # Relación con Reserva
    reserva = models.ForeignKey(
        'ReservaModel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='reserva_id'
    )
    
    # Empleado asignado (mesero o cajero)
    empleado_asignado = models.ForeignKey(
        'User', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        db_column='empleado_id',
        related_name='pedidos_asignados'
    )
    
    comentarios = models.TextField(max_length=500, null=True, blank=True)
    total = models.FloatField(default=0.0)
    estado = models.CharField(max_length=50, default='PENDIENTE')
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pedidos'
        app_label = 'users'

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.numero_mesa}"