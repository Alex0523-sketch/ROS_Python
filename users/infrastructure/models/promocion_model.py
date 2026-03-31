from django.db import models

class PromocionModel(models.Model):
    id_promocion = models.AutoField(primary_key=True, db_column='id_promocion')
    titulo = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    
    # Double en Java -> DecimalField o FloatField en Python
    descuento = models.FloatField(null=False)
    
    # @Temporal(TemporalType.DATE)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @ManyToMany con JoinTable
    # Django creará automáticamente la tabla intermedia 'promocion_productos'
    productos = models.ManyToManyField(
        'ProductoModel', 
        related_name='promociones',
        db_table='promocion_productos' 
    )

    class Meta:
        db_table = 'promociones' # @Table(name = "promociones")
        app_label = 'users'

    def __str__(self):
        return self.titulo