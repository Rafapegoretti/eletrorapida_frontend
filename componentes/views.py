from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from django.conf import settings

API_URL = settings.API_URL


def lista_componentes(request):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}
    busca = request.GET.get("busca", "").strip()

    try:
        if busca:
            url = f"{API_URL}/components/search/?term={busca}"
        else:
            url = f"{API_URL}/components/"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            componentes = response.json()
        else:
            messages.error(request, "Erro ao carregar componentes.")
            componentes = []

    except Exception as e:
        messages.error(request, f"Erro inesperado: {str(e)}")
        componentes = []

    return render(
        request, "componentes/lista.html", {"componentes": componentes, "busca": busca}
    )


def criar_componente(request):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        # Campos de texto
        data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "quantity": request.POST.get("quantity"),
            "location_reference": request.POST.get("location_reference"),
        }

        # Arquivos
        files = {}
        image = request.FILES.get("product_image")
        datasheet = request.FILES.get("datasheet")

        if image:
            files["product_image"] = image
        if datasheet:
            files["datasheet"] = datasheet

        try:
            response = requests.post(
                f"{API_URL}/components/", headers=headers, data=data, files=files
            )
            if response.status_code == 201:
                messages.success(request, "Componente criado com sucesso.")
                return redirect("componentes:lista")
            else:
                messages.error(
                    request, f"Erro ao criar componente. Código: {response.status_code}"
                )
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")

    return render(request, "componentes/form.html")


def editar_componente(request, id):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}

    # buscar dados do componente
    response = requests.get(f"{API_URL}/components/{id}/", headers=headers)
    if response.status_code != 200:
        messages.error(request, "Componente não encontrado.")
        return redirect("componentes:lista")

    componente = response.json()

    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "quantity": request.POST.get("quantity"),
            "location_reference": request.POST.get("location_reference"),
        }

        files = {}
        image = request.FILES.get("product_image")
        datasheet = request.FILES.get("datasheet")

        if image:
            files["product_image"] = image
        if datasheet:
            files["datasheet"] = datasheet

        print(data)

        try:
            response = requests.put(
                f"{API_URL}/components/{id}/", headers=headers, data=data, files=files
            )
            if response.status_code == 200:
                messages.success(request, "Componente atualizado com sucesso.")
                return redirect("componentes:lista")
            else:
                messages.error(request, "Erro ao atualizar o componente.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")

    return render(request, "componentes/form.html", {"componente": componente})


def excluir_componente(request, id):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        try:
            response = requests.delete(f"{API_URL}/components/{id}/", headers=headers)
            if response.status_code == 204:
                messages.success(request, "Componente excluído com sucesso.")
            else:
                messages.error(request, "Erro ao excluir o componente.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")

        return redirect("componentes:lista")

    response = requests.get(f"{API_URL}/components/{id}/", headers=headers)
    if response.status_code == 200:
        componente = response.json()
        return render(
            request, "componentes/confirmar_exclusao.html", {"componente": componente}
        )
    else:
        messages.error(request, "Componente não encontrado.")
        return redirect("componentes:lista")


def detalhar_componente(request, id):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{API_URL}/components/{id}/", headers=headers)
        if response.status_code == 200:
            componente = response.json()
            print(componente)
            return render(
                request, "componentes/detalhe.html", {"componente": componente}
            )
        else:
            messages.error(request, "Componente não encontrado.")
            return redirect("componentes:lista")
    except Exception as e:
        messages.error(request, f"Erro inesperado: {str(e)}")
        return redirect("componentes:lista")
