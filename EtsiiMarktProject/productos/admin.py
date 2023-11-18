from django.contrib import admin
from .models import Categoria, Fabricante, Producto

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Fabricante)
