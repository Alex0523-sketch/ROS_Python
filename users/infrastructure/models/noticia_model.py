from django.db import models

class NoticiaModel(models.Model):
    # Django maneja el ID automáticamente como primary key
    titulo = models.CharField(max_length=150, null=False)
    
    # columnDefinition = "TEXT" -> TextField
    contenido = models.TextField(null=False)
    
    imagen = models.CharField(max_length=255, null=True, blank=True)
    
    # TemporalType.DATE
    fecha_publicacion = models.DateField(null=True, blank=True)
    
    # TemporalType.TIMESTAMP con valor por defecto al actualizar
    # auto_now=True se encarga de actualizar la fecha automáticamente cada vez que se guarda
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'noticias'
        app_label = 'users'

    def __str__(self):
        return self.titulo