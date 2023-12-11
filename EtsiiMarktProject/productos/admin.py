from django.contrib import admin
from .models import Categoria, Fabricante, Opinion, Producto

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Fabricante)
admin.site.register(Opinion)

