from django.db import models

class CategoriaModel(models.Model):
    # id_categoria con incremento automático
    id_categoria = models.AutoField(primary_key=True, db_column='id_categoria')
    
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    
    # Auditoría: created_at no se actualiza (updatable=false)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # updated_at se actualiza en cada save()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categorias'  # @Table(name = "categorias")
        app_label = 'users'

    def __str__(self):
        return self.nombre