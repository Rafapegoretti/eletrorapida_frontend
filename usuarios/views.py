# usuarios/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
import requests


class UsuariosView(View):
    """
    Controlador das operações relacionadas a usuários do sistema.
    """

    def _get_token(self, request):
        token = request.session.get("access")
        if not token:
            messages.error(request, "Acesso negado. Faça login.")
        return token

    def listar(self, request):
        """
        [GET] Lista todos os usuários cadastrados.
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        try:
            response = requests.get(
                f"{settings.API_URL}/users/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                usuarios = response.json()
                return render(request, "usuarios/lista.html", {"usuarios": usuarios})
            messages.error(request, "Erro ao buscar usuários.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {e}")

        return redirect("dashboard:index")

    def criar(self, request):
        """
        [GET] Exibe o formulário de criação de usuário.
        [POST] Cria um novo usuário com os dados fornecidos.
        Campos esperados:
            - name
            - email
            - password
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        if request.method == "POST":
            dados = {
                "username": request.POST.get("name"),
                "email": request.POST.get("email"),
                "password": request.POST.get("password"),
            }
            try:
                response = requests.post(
                    f"{settings.API_URL}/users/",
                    headers={"Authorization": f"Bearer {token}"},
                    data=dados
                )
                if response.status_code == 201:
                    messages.success(request, "Usuário criado com sucesso!")
                    return redirect("usuarios:lista")
                messages.error(request, "Erro ao criar usuário.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")

        return render(request, "usuarios/form.html")

    def editar(self, request, id):
        """
        [GET] Busca os dados de um usuário para edição.
        [POST] Atualiza os dados do usuário (nome, email e opcionalmente senha).
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        if request.method == "POST":
            dados = {
                "username": request.POST.get("name"),
                "email": request.POST.get("email"),
            }
            if request.POST.get("password"):
                dados["password"] = request.POST.get("password")

            try:
                response = requests.patch(
                    f"{settings.API_URL}/users/{id}/",
                    headers={"Authorization": f"Bearer {token}"},
                    data=dados
                )
                if response.status_code == 200:
                    messages.success(request, "Usuário atualizado com sucesso!")
                    return redirect("usuarios:lista")
                messages.error(request, "Erro ao atualizar usuário.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")

        # GET ou erro: carregar dados
        response = requests.get(
            f"{settings.API_URL}/users/{id}/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            usuario = response.json()
            return render(request, "usuarios/form.html", {"usuario": usuario})

        messages.error(request, "Usuário não encontrado.")
        return redirect("usuarios:lista")

    def excluir(self, request, id):
        """
        [GET] Mostra tela de confirmação para exclusão de usuário.
        [POST] Envia requisição de exclusão para a API.
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        if request.method == "POST":
            try:
                response = requests.delete(
                    f"{settings.API_URL}/users/{id}/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 204:
                    messages.success(request, "Usuário excluído com sucesso!")
                else:
                    messages.error(request, "Erro ao excluir usuário.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")
            return redirect("usuarios:lista")

        response = requests.get(
            f"{settings.API_URL}/users/{id}/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            usuario = response.json()
            return render(request, "usuarios/confirmar_exclusao.html", {"usuario": usuario})

        messages.error(request, "Usuário não encontrado.")
        return redirect("usuarios:lista")
