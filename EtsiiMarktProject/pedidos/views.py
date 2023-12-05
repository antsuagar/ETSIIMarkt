import uuid
from django.shortcuts import get_object_or_404, render, redirect

from .models import DireccionEnvio, Pedido, ProductoPedido
from django.contrib import messages
from productos.models import Producto
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
            nuevo_pedido, created = Pedido.objects.get_or_create(user=None,id_transaccion=anonimo_id)
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


def formulario_envio(request):

    return render(request, 'envios/formulario_envio.html')

def procesar_pedido(request):
    
    email = request.POST.get('email')
    direccion = request.POST.get('direccion')
    ciudad = request.POST.get('ciudad')
    codigo_postal = request.POST.get('postal')


    transaccion_id = request.POST.get('transaccion_id')

        # Obtiene la fecha y hora actuales
    fecha_pedido = datetime.now()

    if request.user.is_authenticated:
        user=request.user
        pedido = get_object_or_404(Pedido, user=user)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        user = None
        del request.session['anonimo_id']

  
    direccion_pedido, created = DireccionEnvio.objects.get_or_create(user=user, pedido=pedido, direccion=direccion, ciudad=ciudad, codigo_postal=codigo_postal)
    pedido.fecha_pedido = fecha_pedido
    pedido.completado = True
    pedido.id_transaccion = transaccion_id

    direccion_pedido.save()
    pedido.save()

    id_pedido = pedido.id 
    
    print(id_pedido)
    messages.success(request, 'El pedido se ha completado correctamente, se ha enviado un correo con el seguimiento y puede acceder a el con el siguiente enlace: .../seguimiento/producto_id')

    # Mandar email aqui

    return render(request, 'home.html')
