"""
URL configuration for EtsiiMarkt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from clientes.views import RegistroClienteView
from clientes.views import IniciarSesionView, modificar_datos_usuario, perfil, register
from django.contrib.auth.views import LogoutView
from core.views import index, nosotros, devoluciones
from productos.views import catalogo, catalogo2
from pedidos.views import procesar_pago, exito, error
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('catalogo/', catalogo, name='catalogo'),
    path('busqueda/', catalogo2, name='catalogo2'),
    path('login/', IniciarSesionView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', register, name='registro_usuario'),
    path('perfil/', perfil, name='perfil_usuario'),
    path('modificar_perfil/', modificar_datos_usuario, name='modificar_perfil'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('exito/<str:cantidad>/', exito, name='exito'),
    path('error/<str:error>/', error, name='error'),
    path('nosotros', nosotros, name='nosotros'),
    path('devoluciones', devoluciones, name='devoluciones'),
]
    

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
