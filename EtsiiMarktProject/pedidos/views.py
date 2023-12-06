from django.shortcuts import render
from django.conf import settings
import stripe
from django.http import HttpResponseRedirect
from django.urls import reverse

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

# Pasarela de pago

stripe.api_key = 'sk_test_51OJe72EuWRxRJueoRLXhuB2us5H5nJFQRn02WrVfTyGtZGVopiWMyfDJHk7y0mD7wVXnKPL5UXn7lkoIwjafoemJ0022EMLQvB'

def procesar_pago(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        token = request.POST.get('stripeToken')
        cantidad = request.POST.get('cantidad')

        try:
            # Crear un cargo en Stripe
            cargo = stripe.Charge.create(
                amount=int(cantidad),
                currency='eur',  # Puedes cambiar a la moneda que prefieras
                description='Pago de prueba',
                source=token,
            )

            # Redirigir a la página de éxito si el pago se procesa correctamente
            #return redirect(reverse('exito'), amount=cargo.amount, currency=cargo.currency)
            url = reverse('exito', kwargs={'cantidad':cargo.amount})
            return HttpResponseRedirect(url)

        except stripe.error.CardError as e:
            # El pago ha sido rechazado por Stripe, redirigir a la página de error
            #error_msg = e.error.message
            #return redirect('error', error=error_msg)
            url = reverse('error', kwargs={'error':e.error.message})
            return HttpResponseRedirect(url)            

    return render(request, 'pedidos/payment.html')

def exito(request, cantidad):
    context = {'cantidad': cantidad}
    return render(request, 'pedidos/payment_success.html', context)

def error(request, error):
    #error_msg = request.GET.get('error', 'Error en el pago')
    context = {'error': error}
    return render(request, 'pedidos/payment_failure.html', context)