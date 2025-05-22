from django.urls import path
from .views import ComponentesView

view = ComponentesView()

app_name = "componentes"

urlpatterns = [
    path("", view.listar, name="lista"),
    path("novo/", view.criar, name="criar"),
    path("editar/<int:id>/", view.editar, name="editar"),
    path("excluir/<int:id>/", view.excluir, name="excluir"),
    path("detalhe/<int:id>/", view.detalhar, name="detalhe"),
]