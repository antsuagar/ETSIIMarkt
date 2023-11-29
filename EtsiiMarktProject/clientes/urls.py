from django.contrib import admin
from django.urls import include, path

from .models import Producto
from .views import catalogo, detalle, index
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    
        path('home', index, name='index'),
]