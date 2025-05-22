# login/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.conf import settings
import requests


class LoginView(View):
    """
    Controlador de autenticação do sistema.
    Responsável por login, logout e recuperação de senha.
    """

    def login(self, request):
        """
        [GET] Renderiza tela de login.
        [POST] Realiza autenticação com username e password.
        Armazena tokens na sessão:
            - request.session["access"]
            - request.session["refresh"]
        Redireciona para /dashboard/ em caso de sucesso.
        """
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            try:
                response = requests.post(
                    f"{settings.API_URL}/auth/login/",
                    data={"username": username, "password": password},
                )

                if response.status_code == 200:
                    data = response.json()
                    request.session["access"] = data["access"]
                    request.session["refresh"] = data["refresh"]
                    return redirect("/dashboard/")
                messages.error(request, "Usuário ou senha inválidos.")
            except Exception as e:
                messages.error(request, f"Erro ao autenticar: {e}")

        return render(request, "login/login.html")

    def logout(self, request):
        """
        [GET] Realiza logout limpando a sessão do usuário.
        Redireciona para a tela de login.
        """
        request.session.flush()
        return redirect("login:login")

    def password_reset(self, request):
        """
        [GET] Exibe o formulário para inserir e-mail.
        [POST] Envia requisição para envio de link de redefinição de senha.
        """
        if request.method == "POST":
            email = request.POST.get("email")
            try:
                response = requests.post(
                    f"{settings.API_URL}/auth/password/reset/", data={"email": email}
                )
                if response.status_code == 200:
                    messages.success(
                        request,
                        "Se o e-mail estiver cadastrado, enviaremos um link de redefinição.",
                    )
                    return redirect("login:login")
                else:
                    messages.error(request, "Erro ao tentar enviar o e-mail.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")

        return render(request, "login/password_reset.html")

    def password_reset_confirm(self, request):
        """
        [GET] Renderiza formulário para nova senha.
        [POST] Envia nova senha para o backend, usando `uid` e `token` da URL.
        """
        if request.method == "POST":
            uid = request.POST.get("uid")
            token = request.POST.get("token")
            new_password = request.POST.get("new_password")

            data = {"uid": uid, "token": token, "new_password": new_password}

            try:
                response = requests.post(
                    f"{settings.API_URL}/auth/password/reset/confirm/", data=data
                )
                if response.status_code == 200:
                    messages.success(request, "Senha redefinida com sucesso.")
                    return redirect("login:login")
                messages.error(request, "Erro ao redefinir a senha. Verifique os dados.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {e}")

        return render(request, "login/password_reset_confirm.html")
