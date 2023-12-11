from django.db import models

from django.db import models
from django.contrib.auth.models import User


class DireccionCliente(models.Model):

    PAGO_CHOICES = [
        ('contrarrempolso', 'Contrareenbolso'),
        ('pasarela', 'Tarjeta de crédito'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    postal = models.CharField(max_length=10)
    formaPago = models.CharField(max_length=50, choices=PAGO_CHOICES, default='contrarrempolso', verbose_name="Método preferido de pago")

    def __str__(self):
        return f"Dirección de {self.user}"  
    
