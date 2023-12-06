from django.db import models
from django.contrib.auth.models import User

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
    
class Fabricante(models.Model):
    nombre = models.CharField(max_length=100)

    @classmethod
    def get_default_fabricante(cls):
        fabricante, created = cls.objects.get_or_create(
            nombre='Fabricante', 
        )
        return fabricante.pk
    
    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Fabricantes'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,related_name='productos', on_delete=models.SET_DEFAULT, default=Categoria.get_default_categoria)
    fabricante = models.ForeignKey(Fabricante,related_name='productos', on_delete=models.SET_DEFAULT, default=Fabricante.get_default_fabricante)
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField(default=1)
    imagen = models.ImageField(upload_to='productos_imagenes', blank=True, null=True)
    
    @property
    def producto_agotado(self):
        return self.cantidad == 0
    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre
    
    def venta(self, cantidad_vendida):
        return self.cantidad-cantidad_vendida
    
    def get_productos_by_categoria(categoria):
        if categoria:
            return Producto.objects.filter(categoria=categoria)
        else: 
            return Producto.objects.all()
        
    def get_productos_by_fabricante(fabricante):
        if fabricante:
            return Producto.objects.filter(fabricante=fabricante)
        else:
            return Producto.objects.all()
        
    def get_productos_by_precio(precio_min, precio_max):
        return Producto.objects.filter(precio__range=(precio_min, precio_max))
    
class Opinion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    cuerpo = models.CharField(max_length=500)

    class Meta:
        ordering = ['producto']
        verbose_name_plural = 'Opiniones'

    def __str__(self):
        return self.producto.nombre+ ": " + self.user.username
    
class ProductoManager(models.Manager):

    def createProducto(self, producto):
        producto=self.create(nombre=producto.nombre, precio=producto.precio)
        return producto



