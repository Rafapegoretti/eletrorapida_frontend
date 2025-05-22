from django.urls import path
from .views import UsuariosView

view = UsuariosView()

app_name = "usuarios"

urlpatterns = [
    path("", view.listar, name="lista"),
    path("novo/", view.criar, name="criar"),
    path("editar/<int:id>/", view.editar, name="editar"),
    path("excluir/<int:id>/", view.excluir, name="excluir"),
]