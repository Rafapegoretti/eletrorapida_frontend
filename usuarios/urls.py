from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.lista_usuarios, name="lista"),
    path("novo/", views.criar_usuario, name="criar"),
    path("editar/<int:id>/", views.editar_usuario, name="editar"),
    path("excluir/<int:id>/", views.excluir_usuario, name="excluir"),
]
