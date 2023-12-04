import uuid
from django.shortcuts import get_object_or_404, render

from .models import Pedido, ProductoPedido
from productos.models import Fabricante, Producto, Categoria

# Create your views here.
def carrito(request):

    if request.user.is_authenticated:
        user=request.user
        pedido = Pedido.objects.get_or_create(user=user)
        items = pedido.get_productos_carrito() 
    else:
        if 'anonimo_id' not in request.session:
            request.session['anonimo_id'] = str(uuid.uuid4())
            anonimo_id = request.session['anonimo_id']
            nuevo_pedido = Pedido(user=None,id_transaccion=anonimo_id)
            nuevo_pedido.save()
            items = []
            pedido = {'get_total_carrito':0, 'get_productos_carrito':0}
                
               
        else:
            anonimo_id = request.session['anonimo_id']
            pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
            items = pedido.get_productos_carrito()
            
          
        

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)