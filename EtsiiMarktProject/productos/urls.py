from django.contrib import admin
from django.urls import include, path
from .views import catalogo, detalle_producto
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [    

    #path("admin/", admin.site.urls),
    path("catalogo/", catalogo, name='catalogo'),
    path('catalogo/<int:producto_id>/', detalle_producto, name='detalle_producto'),
]
