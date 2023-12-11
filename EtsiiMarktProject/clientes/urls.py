from django.contrib import admin
from django.urls import include, path

from .models import Producto
from .views import catalogo, detalle, editar_direccion_envio, index
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
        path('home', index, name='index'),
        path('editar_direccion_envio', editar_direccion_envio, name='editar_direccion_envio'),
]