from django.shortcuts import render, redirect
import requests
from django.contrib import messages

API_URL = "http://127.0.0.1:8000"


def lista_usuarios(request):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Acesso negado. Faça login.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{API_URL}/users/", headers=headers)
        if response.status_code == 200:
            usuarios = response.json()
            return render(request, "usuarios/lista.html", {"usuarios": usuarios})
        else:
            messages.error(request, "Erro ao buscar usuários.")
    except Exception as e:
        messages.error(request, f"Erro inesperado: {e}")

    return redirect("dashboard:index")


def criar_usuario(request):
    if request.method == "POST":
        token = request.session.get("access")
        headers = {"Authorization": f"Bearer {token}"}
        dados = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }
        response = requests.post(f"{API_URL}/users/", headers=headers, data=dados)
        if response.status_code == 201:
            messages.success(request, "Usuário criado com sucesso!")
            return redirect("usuarios:lista")
        else:
            messages.error(request, "Erro ao criar usuário.")

    return render(request, "usuarios/form.html")


def editar_usuario(request, id):
    token = request.session.get("access")
    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        dados = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
        }
        if request.POST.get("password"):
            dados["password"] = request.POST.get("password")

        response = requests.patch(f"{API_URL}/users/{id}/", headers=headers, data=dados)
        if response.status_code == 200:
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("usuarios:lista")
        else:
            messages.error(request, "Erro ao atualizar usuário.")

    response = requests.get(f"{API_URL}/users/{id}/", headers=headers)
    if response.status_code == 200:
        usuario = response.json()
        return render(request, "usuarios/form.html", {"usuario": usuario})

    messages.error(request, "Usuário não encontrado.")
    return redirect("usuarios:lista")


def excluir_usuario(request, id):
    token = request.session.get("access")
    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        response = requests.delete(f"{API_URL}/users/{id}/", headers=headers)
        if response.status_code == 204:
            messages.success(request, "Usuário excluído com sucesso!")
        else:
            messages.error(request, "Erro ao excluir usuário.")
        return redirect("usuarios:lista")

    response = requests.get(f"{API_URL}/users/{id}/", headers=headers)
    if response.status_code == 200:
        usuario = response.json()
        return render(request, "usuarios/confirmar_exclusao.html", {"usuario": usuario})

    messages.error(request, "Usuário não encontrado.")
    return redirect("usuarios:lista")
