from django.contrib import admin
from django.urls import include, path

from pedidos.views import carrito

from .models import Producto
from .views import catalogo, detalle
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    

    #path("admin/", admin.site.urls),
    path("catalogo/", catalogo, name='catalogo'),
    path('detalle/<int:producto_id>/', detalle, name='detalle'),
    path("carrito/", carrito, name='carrito'),
]
