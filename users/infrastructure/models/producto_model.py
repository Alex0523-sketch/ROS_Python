from django.db import models

class ProductoModel(models.Model):
    id_producto = models.AutoField(primary_key=True, db_column='id_producto')
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    
    # Double en Java -> FloatField o DecimalField (recomendado para dinero)
    precio = models.FloatField(null=False)
    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @ManyToOne -> ForeignKey
    categoria = models.ForeignKey(
        'CategoriaModel', 
        on_delete=models.CASCADE, 
        db_column='id_categoria'
    )

    # Nota: En Django, la relación ManyToMany se define en un solo lado.
    # Como ya la definimos en PromocionModel, aquí no es necesario 
    # declararla de nuevo. Accederás a las promociones de un producto 
    # mediante el 'related_name' definido en PromocionModel (promociones).

    class Meta:
        db_table = 'productos'
        app_label = 'users'

    def __str__(self):
        return self.nombre