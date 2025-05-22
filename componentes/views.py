from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.conf import settings
import requests


class ComponentesView(View):
    """
    Controlador das operações relacionadas a componentes eletrônicos.
    """

    def _get_token(self, request):
        """
        Recupera o token de autenticação da sessão do usuário.
        Exibe erro se não houver token válido.
        """
        token = request.session.get("access")
        if not token:
            messages.error(request, "Você precisa estar logado.")
        return token

    def listar(self, request):
        """
        [GET] Lista os componentes cadastrados.
        Se um termo for informado via querystring `?busca=...`, realiza a busca filtrada.
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        busca = request.GET.get("busca", "").strip()
        try:
            if busca:
                url = f"{settings.API_URL}/components/search/?term={busca}"
            else:
                url = f"{settings.API_URL}/components/"
            response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
            componentes = response.json() if response.status_code == 200 else []
            if response.status_code != 200:
                messages.error(request, "Erro ao carregar componentes.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            componentes = []

        return render(request, "componentes/lista.html", {"componentes": componentes, "busca": busca})

    def criar(self, request):
        """
        [GET] Renderiza o formulário de novo componente.
        [POST] Envia os dados para criação do componente via API.
        Campos esperados:
            - name
            - description
            - quantity
            - location_reference
            - product_image (arquivo)
            - datasheet (arquivo)
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        if request.method == "POST":
            data = {
                "name": request.POST.get("name"),
                "description": request.POST.get("description"),
                "quantity": request.POST.get("quantity"),
                "location_reference": request.POST.get("location_reference"),
            }
            files = {}
            if request.FILES.get("product_image"):
                files["product_image"] = request.FILES["product_image"]
            if request.FILES.get("datasheet"):
                files["datasheet"] = request.FILES["datasheet"]

            try:
                response = requests.post(
                    f"{settings.API_URL}/components/",
                    headers={"Authorization": f"Bearer {token}"},
                    data=data,
                    files=files
                )
                if response.status_code == 201:
                    messages.success(request, "Componente criado com sucesso.")
                    return redirect("componentes:lista")
                messages.error(request, "Erro ao criar componente.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {str(e)}")

        return render(request, "componentes/form.html")

    def editar(self, request, id):
        """
        [GET] Busca os dados do componente para edição.
        [POST] Atualiza os dados do componente via API.
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        if request.method == "POST":
            data = {
                "name": request.POST.get("name"),
                "description": request.POST.get("description"),
                "quantity": request.POST.get("quantity"),
                "location_reference": request.POST.get("location_reference"),
            }
            files = {}
            if request.FILES.get("product_image"):
                files["product_image"] = request.FILES["product_image"]
            if request.FILES.get("datasheet"):
                files["datasheet"] = request.FILES["datasheet"]

            try:
                response = requests.put(
                    f"{settings.API_URL}/components/{id}/",
                    headers={"Authorization": f"Bearer {token}"},
                    data=data,
                    files=files
                )
                if response.status_code == 200:
                    messages.success(request, "Componente atualizado com sucesso.")
                    return redirect("componentes:lista")
                messages.error(request, "Erro ao atualizar componente.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {str(e)}")

        # GET ou erro: renderiza formulário com dados atuais
        response = requests.get(
            f"{settings.API_URL}/components/{id}/",
            headers={"Authorization": f"Bearer {token}"}
        )
        componente = response.json() if response.status_code == 200 else {}
        return render(request, "componentes/form.html", {"componente": componente})

    def excluir(self, request, id):
        """
        [GET] Mostra confirmação de exclusão.
        [POST] Realiza exclusão via API.
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        if request.method == "POST":
            try:
                response = requests.delete(
                    f"{settings.API_URL}/components/{id}/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 204 or response.status_code == 200:
                    messages.success(request, "Componente excluído com sucesso.")
                else:
                    messages.error(request, "Erro ao excluir o componente.")
            except Exception as e:
                messages.error(request, f"Erro inesperado: {str(e)}")
            return redirect("componentes:lista")

        # GET
        response = requests.get(
            f"{settings.API_URL}/components/{id}/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            componente = response.json()
            return render(request, "componentes/confirmar_exclusao.html", {"componente": componente})

        messages.error(request, "Componente não encontrado.")
        return redirect("componentes:lista")

    def detalhar(self, request, id):
        """
        [GET] Exibe detalhes do componente identificado por ID.
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        try:
            response = requests.get(
                f"{settings.API_URL}/components/{id}/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                componente = response.json()
                return render(request, "componentes/detalhe.html", {"componente": componente})
            messages.error(request, "Componente não encontrado.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
        return redirect("componentes:lista")