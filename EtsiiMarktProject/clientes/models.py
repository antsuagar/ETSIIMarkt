from django.db import models

from django.db import models
from django.contrib.auth.models import User


class DireccionCliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    postal = models.CharField(max_length=10)

    def __str__(self):
        return f"Dirección de {self.user}"  
    
