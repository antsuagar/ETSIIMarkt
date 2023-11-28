from django.contrib import admin

from pedidos.models import DireccionEnvio, Pedido, ProductoPedido

# Register your models here.
admin.site.register(Pedido)
admin.site.register(ProductoPedido)
admin.site.register(DireccionEnvio)
