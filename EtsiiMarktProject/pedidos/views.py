import uuid
from django.shortcuts import get_object_or_404, render, redirect

from .models import Pedido, ProductoPedido
from productos.models import Fabricante, Producto, Categoria
from datetime import datetime 

# Create your views here.
def carrito(request):

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
        items = pedido.get_lista_de_productos_carrito() 
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
            items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)

def actualizar(request, producto_id):
    q_cantidad = request.POST.get('cantidad', '1')
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)

    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    producto_pedido.cantidad = q_cantidad
    producto_pedido.save()   

    items = pedido.get_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def eliminar(request, producto_id):
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        
        
            
    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    producto_pedido.delete()   

    items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def formulario_envio(request, id_transaccion):
    # Lógica para manejar el formulario de envío
    return render(request, 'formulario_envio.html', {'id_transaccion': id_transaccion})

def procesar_pedido(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        transaccion_id = request.POST.get('transaccion_id')
        completado = request.POST.get('completado')

        # Obtiene la fecha y hora actuales
        fecha_pedido = datetime.now()

        # Crea un nuevo objeto Pedido con los datos del formulario y la fecha actual
        pedido = Pedido.objects.create(
            
            fecha_pedido=fecha_pedido,
            completado=completado,
            transaccion_id=transaccion_id,
           
            # Otros campos del pedido
        )

        # Lógica adicional, como enviar correos electrónicos, actualizar inventarios, etc.

        return redirect('home')
