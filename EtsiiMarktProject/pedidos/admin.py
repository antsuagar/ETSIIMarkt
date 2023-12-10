from django.contrib import admin

from pedidos.models import DireccionEnvio, Pedido, ProductoPedido, Reclamacion

# Register your models here.
admin.site.register(Pedido)
admin.site.register(Reclamacion)
admin.site.register(ProductoPedido)
admin.site.register(DireccionEnvio)
