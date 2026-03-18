from django.db import models

class RolModel(models.Model):
    # primary_key=True implica nullable=False y unique=True automáticamente
    id_rol = models.AutoField(primary_key=True, db_column='id_rol')
    
    # max_length=50 y unique=True como en tu código Java
    nombre = models.CharField(max_length=50, unique=True, null=False)

    class Meta:
        db_table = 'rol'  # @Table(name = "rol")
        app_label = 'users'

    def __str__(self):
        return self.nombre