from enum import Enum
from django.db import models

from productos.models import Producto

from django.contrib.auth.models import User

# Create your models here.
class EstadoProducto(Enum):
    EN_PREPARACION = 'En preparación'
    ENVIADO = 'Enviado'
    ENTREGADO = 'Entregado'

    
class Pedido(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pedido=models.DateTimeField(auto_now_add=True)
    completado=models.BooleanField(default=False)
    id_transaccion=models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=20, choices=[(estado.value, estado.value) for estado in EstadoProducto], null=True, blank=True)


    @property
    def get_total_carrito(self):
        productopedidos=self.productopedido_set.all()
        total=sum([p.get_total for p in productopedidos])
        return total
    
    @property
    def get_productos_carrito(self):
        productopedidos=self.productopedido_set.all()
        total=sum([p.cantidad for p in productopedidos])
        return total
    
    def get_estado(self):
        if str(EstadoProducto.EN_PREPARACION)==self.estado:
            return 'En preparación'
        if str(EstadoProducto.ENTREGADO)==self.estado:
            return 'Entregado'
        if str(EstadoProducto.ENVIADO)==self.estado:
            return 'Enviado'
    
    def get_lista_de_productos_carrito(self):
        productos = [producto_pedido for producto_pedido in self.productopedido_set.all()]
        return productos

    def __str__(self):
        return str(self.id)

class ProductoPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    pedido= models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total=self.producto.precio*self.cantidad
        return total

class DireccionEnvio(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=200, null=False)
    ciudad = models.CharField(max_length=200, null=False)
    codigo_postal= models.CharField(max_length=200, null=False)
    
    def __str__(self):
        return self.direccion

class Reclamacion(models.Model):
    ESTADO_CHOICES = [
        ('por_resolver', 'Por Resolver'),
        ('en_proceso', 'En Proceso'),
        ('solucionado', 'Solucionado'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=False)
    cuerpo = models.CharField(max_length=500)
    resolucion = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='por_resolver', verbose_name="Estado de la Reclamación")

    class Meta:
        ordering = ['pedido']
        verbose_name_plural = 'Reclamaciones'

    def __str__(self):
        return f"Reclamación de {self.pedido.user.username} en el pedido {self.pedido.id}"