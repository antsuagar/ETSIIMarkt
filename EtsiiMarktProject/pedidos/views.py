from django.shortcuts import render

from .models import Pedido, ProductoPedido

# Create your views here.
def carrito(request):
    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user, complete=False)
        items = pedido.productos_set.all()
    else:
        items = []
        pedido = {'get_total_carrito':0, 'get_productos_carrito':0}

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)