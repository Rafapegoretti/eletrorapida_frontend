from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("login.urls")),
    path("componentes/", include("componentes.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("admin/", admin.site.urls),
]
