from django.db import models

class HorarioModel(models.Model):
    # Relación con el empleado (User)
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        db_column='user_id',
        related_name='horarios_empleado'
    )
    
    dia_semana = models.CharField(max_length=20, null=False) # Lunes, Martes, etc.
    hora_inicio = models.CharField(max_length=5, null=False) # "08:00"
    hora_fin = models.CharField(max_length=5, null=False)    # "17:00"
    
    # Timestamps de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'horarios'
        app_label = 'users'

    def __str__(self):
        return f"{self.user.nombre} - {self.dia_semana} ({self.hora_inicio}-{self.hora_fin})"