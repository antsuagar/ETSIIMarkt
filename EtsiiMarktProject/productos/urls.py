from django.contrib import admin
from django.urls import include, path

from . import views
from productos.views import index

urlpatterns = [    
    path("", index),
    path("admin/", admin.site.urls),
]