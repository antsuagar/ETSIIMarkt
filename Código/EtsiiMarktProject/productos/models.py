from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    @classmethod
    def get_default_categoria(cls):
        categoria, created = cls.objects.get_or_create(
            nombre='Electrodomestico', 
        )
        return categoria.pk
    
    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria=models.ForeignKey(Categoria,related_name='productos', on_delete=models.CASCADE, default=Categoria.get_default_categoria)
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    agotado=models.BooleanField(default=False)
    imagen=models.ImageField(upload_to='productos_imagenes', blank=True, null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre

class ProductoManager(models.Manager):

    def createProducto(self, producto):
        producto=self.create(nombre=producto.nombre, precio=producto.precio, descripcion=producto, fabricante=producto.fabricante)
        return producto


