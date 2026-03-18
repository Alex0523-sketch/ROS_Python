from django.db import models
from django.utils import timezone

class User(models.Model):
    # En Django, el ID se crea automáticamente, pero si quieres el nombre exacto:
    id_user = models.AutoField(primary_key=True, db_column='id_user')
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    
    activo = models.BooleanField(default=True)
    
    # Equivalente a @Temporal(TemporalType.TIMESTAMP) y updatable=False
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Relación @ManyToOne con Rol
    # Suponiendo que tu modelo Rol está en el mismo archivo o importado
    rol = models.ForeignKey('Rol', on_delete=models.PROTECT, db_column='id_rol', null=True)

    class Meta:
        db_table = 'users'  # Equivalente a @Table(name = "users")
        app_label = 'users'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"