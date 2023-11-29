from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True, default='correo@ejemplo.com')
    nombre = models.CharField(max_length=254, blank=True, null=True, default='Nombre')
    apellido1 = models.CharField(max_length=254, blank=True, null=True, default='Primer apellido')
    apellido2 = models.CharField(max_length=254, blank=True, null=True, default='Segundo apellido')
    direccion = models.CharField(max_length=254, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return self.nombre
