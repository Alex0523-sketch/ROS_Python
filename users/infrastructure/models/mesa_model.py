from django.db import models

class MesaModel(models.Model):
    # Definimos explícitamente id_mesa para que coincida con Java
    id_mesa = models.AutoField(primary_key=True, db_column='id_mesa')
    
    numero_mesa = models.IntegerField(null=False)
    capacidad = models.IntegerField(null=False)
    
    # Ubicación opcional como en tu código Java
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    
    # "libre", "ocupada", "reservada"
    estado = models.CharField(max_length=50, null=False, default='libre')
    
    # Auditoría: registro de cuándo se creó la mesa físicamente
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mesas'
        app_label = 'users'

    def __str__(self):
        return f"Mesa {self.numero_mesa} - Capacidad: {self.capacidad}"