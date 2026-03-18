from django.db import models

class ReservaModel(models.Model):
    # Django crea el 'id' automáticamente, igual que GenerationType.IDENTITY
    codigo_reserva = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Relación ManyToOne con User (nullable=true)
    user = models.ForeignKey(
        'UserModel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='user_id'
    )
    
    # Campos para clientes no registrados
    nombre_cliente = models.CharField(max_length=100, null=True, blank=True)
    email_cliente = models.EmailField(max_length=100, null=True, blank=True)
    telefono_cliente = models.CharField(max_length=20, null=True, blank=True)
    
    # Relación ManyToOne con Mesa (nullable=false)
    mesa = models.ForeignKey(
        'MesaModel', 
        on_delete=models.CASCADE, 
        db_column='mesa_id'
    )
    
    fecha_reserva = models.DateTimeField()
    hora = models.CharField(max_length=10)
    numero_personas = models.IntegerField()
    estado = models.CharField(max_length=50)
    comentarios = models.TextField(max_length=500, null=True, blank=True)
    
    # Timestamps equivalentes a @Temporal
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reserva'
        app_label = 'users'

    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.nombre_cliente or self.user}"