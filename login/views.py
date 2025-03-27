from django.shortcuts import render, redirect
from django.contrib import messages
import requests

API_URL = "http://127.0.0.1:8000"  # sua API local


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(
            f"{API_URL}/auth/login/", data={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            request.session["access"] = data["access"]
            request.session["refresh"] = data["refresh"]
            return redirect("/componentes/")  # depois você muda para o app real
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "login/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login:login")


def password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        response = requests.post(
            f"{API_URL}/auth/password/reset/", data={"email": email}
        )

        if response.status_code == 200:
            messages.success(
                request,
                "Se o e-mail estiver cadastrado, enviaremos um link de redefinição.",
            )
            return redirect("login:login")
        else:
            messages.error(request, "Erro ao tentar enviar o e-mail. Tente novamente.")

    return render(request, "login/password_reset.html")


def password_reset_confirm_view(request):
    if request.method == "POST":
        uid = request.POST.get("uid")
        token = request.POST.get("token")
        new_password = request.POST.get("new_password")

        data = {"uid": uid, "token": token, "new_password": new_password}

        response = requests.post(f"{API_URL}/auth/password/reset/confirm/", data=data)

        if response.status_code == 200:
            messages.success(
                request, "Senha redefinida com sucesso. Faça login novamente."
            )
            return redirect("login:login")
        else:
            messages.error(request, "Erro ao redefinir a senha. Verifique os dados.")

    return render(request, "login/password_reset_confirm.html")
