from django.urls import path
from . import views

app_name = "componentes"

urlpatterns = [
    path("", views.lista_componentes, name="lista"),
    path("novo/", views.criar_componente, name="criar"),
    path("editar/<int:id>/", views.editar_componente, name="editar"),
    path("excluir/<int:id>/", views.excluir_componente, name="excluir"),
    path("detalhe/<int:id>/", views.detalhar_componente, name="detalhe"),
]
