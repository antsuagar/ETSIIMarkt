import uuid
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import stripe

from clientes.models import DireccionCliente

from .models import DireccionEnvio, Pedido, ProductoPedido, EstadoProducto
from django.contrib import messages
from productos.models import Producto
from datetime import datetime 
from django.core.mail import send_mail
from smtplib import SMTPRecipientsRefused
from django.db.models import Q
from .forms import ReclamacionForm
from django.utils import formats
from django.utils import translation
from django.contrib.auth.decorators import login_required
from .models import Reclamacion

def carrito(request):

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
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
    q_montar = request.POST.get('montar_domicilio','False')

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)

    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    q_producto.cantidad = q_producto.cantidad+(producto_pedido.cantidad-int(q_cantidad))
    producto_pedido.cantidad =q_cantidad
    if q_montar!='False':
        producto_pedido.montar_domicilio=True
    else:
        producto_pedido.montar_domicilio=q_montar
    producto_pedido.save() 
    q_producto.save()  

    

    items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def eliminar(request, producto_id):
    q_producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user=request.user
        pedido, created = Pedido.objects.get_or_create(user=user,completado=False)
      
    else:
        anonimo_id = request.session['anonimo_id']
        pedido = get_object_or_404(Pedido, id_transaccion=anonimo_id)
        
        
            
    producto_pedido, createdP= ProductoPedido.objects.get_or_create(pedido=pedido,producto=q_producto)
    q_producto.cantidad = q_producto.cantidad+producto_pedido.cantidad
    producto_pedido.delete()  
    q_producto.save()  

    items = pedido.get_lista_de_productos_carrito()

    context={'items': items, 'pedido': pedido}
    return render(request, 'productos/carrito.html', context)


def formulario_envio(request, pedido_id):
    user = request.user
    if request.user.is_authenticated:
        direccionCliente = DireccionCliente.objects.get(user=user)
        email = user.email
        direccion = direccionCliente.direccion
        ciudad = direccionCliente.ciudad
        postal = direccionCliente.postal
        formaPago = direccionCliente.formaPago
        destinatario = user.first_name + " " + user.last_name
        return render(request, 'envios/formulario_envio.html', {'pedido_id':pedido_id, 'email': email, 'postal': postal, 'direccion': direccion, 'ciudad': ciudad, 'formaPago': formaPago, 'destinatario': destinatario})
    else:
        return render(request, 'envios/formulario_envio.html', {'pedido_id':pedido_id})


    
stripe.api_key = 'sk_test_51OJe72EuWRxRJueoRLXhuB2us5H5nJFQRn02WrVfTyGtZGVopiWMyfDJHk7y0mD7wVXnKPL5UXn7lkoIwjafoemJ0022EMLQvB'

def procesar_pedido(request):
    
    email = request.POST.get('email')
    direccion = request.POST.get('direccion')
    ciudad = request.POST.get('ciudad')
    codigo_postal = request.POST.get('postal')
    pedido_id = request.POST.get('pedido_id')
    forma_pago = request.POST.get('formaPago')
    pagado = request.POST.get('pagado','')
    destinatario = request.POST.get('destinatario')
    pedido = get_object_or_404(Pedido,pk=pedido_id)

    if forma_pago=='pasarela' and pagado=='':
        return render(request, 'pedidos/payment.html', {'pedido':pedido, 'email':email, 'direccion': direccion, 'ciudad':ciudad, 'postal':codigo_postal,'formaPago':forma_pago, 'destinatario': destinatario}) 
    
    elif forma_pago=='pasarela' and pagado=='tarjeta':
        cantidad = request.POST.get('cantidad','0')
        cantidad = cantidad.replace(',', '.')
        amount = float(cantidad)*100
        token = request.POST.get('stripeToken')

        try:
            # Crear un cargo en Stripe
            cargo = stripe.Charge.create(
                amount=int(amount),
                currency='eur',  # Puedes cambiar a la moneda que prefieras
                description='pago etsiimarkt',
                source=token,
                
            )

            # Redirigir a la página de éxito si el pago se procesa correctamente
            #return redirect(reverse('exito'), amount=cargo.amount, currency=cargo.currency)

        except stripe.error.CardError as e:
            # El pago ha sido rechazado por Stripe, redirigir a la página de error
            #error_msg = e.error.message
            #return redirect('error', error=error_msg)
            url = reverse('error', kwargs={'error':e.error.message})
            return HttpResponseRedirect(url)    
        
    emails = [email]


    fecha_pedido = datetime.now()

    if request.user.is_authenticated:
        user=request.user
      
    else:
        user = None
        del request.session['anonimo_id']

    
    id_pedido = pedido.id 
    nombre_productos = [p.producto.nombre for p in pedido.get_lista_de_productos_carrito()]
    total = pedido.get_total_carrito
    factura = ', '.join(nombre_productos)

    try:
        send_mail(
        "Su pedido en Etsii Markt esta en marcha",
        "Gracias por comprar con nosotros, {6}. Le informamos que su pedido de {0} con un total de {1} euros esta en marcha y se enviará a la dirección proporcionada: {2} en {3}, {4}. Podra rastrear su pedido en nuestra página web introduciendo el número de su pedido: {5} en el apartado de Mis pedidos o estando registrado en nuestra web".format(factura, total, direccion, ciudad, codigo_postal, id_pedido, destinatario),
        "etsiiMarktProyect@outlook.es",
        emails,
        fail_silently=False,
        )
    except SMTPRecipientsRefused as e:
        messages.error('Error, la dirección de correo introducida: {0} es invalida'.format(email))
        return render(request, 'envios/formulario_envio.html') 

    direccion_pedido, created = DireccionEnvio.objects.get_or_create(user=user, pedido=pedido, direccion=direccion, ciudad=ciudad, codigo_postal=codigo_postal)
    pedido.fecha_pedido = fecha_pedido
    pedido.completado = True
    if forma_pago=='pasarela':
        pedido.id_transaccion = token
    else:
        pedido.id_transaccion = 'Contrareembolso'
    
    pedido.estado = EstadoProducto.EN_PREPARACION
    direccion_pedido.save()
    pedido.save()


    messages.success(request, 'Su pedido con id: {0}, se ha completado correctamente. Se ha enviado un correo a la dirección indicada con el id de seguimiento y puede hacer el seguimiento de su seguimiento en la pestaña Pedidos realizados'.format(id_pedido))
    
 
    return render(request, 'envios/resultado_envio.html')

def pedidos_usuario(request):
    
    if request.user.is_authenticated:
        user=request.user
        pedidos = Pedido.objects.all().filter(Q(user=user) & Q(completado=True))
        if len(pedidos)==0:
            messages.error(request, 'Aún no ha realizado ningún pedido')
      
    else:
        id_pedido= request.GET.get('idPedido','')
        if id_pedido=='':
            messages.success(request, 'Para poder hacer seguimiento de sus pedidos, registrese o indique número de su pedido')            
            return render(request, 'envios/seguimiento.html')
        pedido = get_object_or_404(Pedido, id=id_pedido)
        pedidos =[pedido]
    
    return render(request, 'envios/seguimiento.html', {'pedidos': pedidos})


def error(request, error):
    #error_msg = request.GET.get('error', 'Error en el pago')
    context = {'error': error}
    return render(request, 'pedidos/payment_failure.html', context)

@login_required
def agregar_reclamacion(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)

    if request.method == 'POST':
        form = ReclamacionForm(request.POST)
        if form.is_valid():
            nueva_reclamacion = form.save(commit=False)
            nueva_reclamacion.user = request.user
            nueva_reclamacion.pedido = pedido
            nueva_reclamacion.save()

            # Obtén la fecha del pedido en el formato deseado
            translation.activate('es')
            fecha_pedido = formats.date_format(pedido.fecha_pedido, "SHORT_DATE_FORMAT")

            # Construye el mensaje de éxito con la fecha del pedido
            mensaje_exito = f'Tu reclamación del pedido con fecha {fecha_pedido} ha sido guardada con éxito.'

            # Agregar el mensaje de éxito
            messages.success(request, mensaje_exito)
            translation.deactivate()

            url = reverse('seguimiento')
            return HttpResponseRedirect(url)
    else:
        form = ReclamacionForm()

    return render(request, 'envios/agregar_reclamacion.html', {'pedido': pedido, 'form': form})

@login_required
def reclamaciones_cliente(request):
    reclamaciones = Reclamacion.objects.filter(pedido__user=request.user)

    return render(request, 'envios/reclamaciones_cliente.html', {'reclamaciones': reclamaciones})

@login_required
def editar_reclamacion(request, reclamacion_id):
    reclamacion = get_object_or_404(Reclamacion, pk=reclamacion_id, pedido__user=request.user)

    if request.method == 'POST':
        form = ReclamacionForm(request.POST, instance=reclamacion)
        if form.is_valid():
            reclamacion.resolucion = 'por_resolver'
            form.save()
            return HttpResponseRedirect(reverse('reclamaciones_cliente'))
    else:
        form = ReclamacionForm(instance=reclamacion)

    return render(request, 'envios/editar_reclamacion.html', {'form': form, 'reclamacion': reclamacion})

def eliminar_reclamacion(request, reclamacion_id):
    reclamacion = get_object_or_404(Reclamacion, pk=reclamacion_id, pedido__user=request.user)

    if request.method == 'POST':
        reclamacion.delete()
        return redirect('reclamaciones_cliente')

    return render(request, 'envios/eliminar_reclamacion.html', {'reclamacion': reclamacion})