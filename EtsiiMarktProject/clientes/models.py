from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True, default='correo@ejemplo.com')
    nombre = models.CharField(max_length=150, blank=True, null=True)
    apellidos = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.nombre:
            return self.nombre
        else:
            return str(self.email)
