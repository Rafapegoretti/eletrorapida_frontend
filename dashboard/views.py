# dashboard/views.py

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests


class DashboardView(View):
    """
    View controladora do Dashboard do sistema.
    Responsável por exibir os dados estatísticos do backend.
    """

    def _get_token(self, request):
        """
        Recupera o token de autenticação da sessão do usuário.
        Exibe uma mensagem e redireciona caso esteja ausente.
        """
        token = request.session.get("access")
        if not token:
            messages.error(request, "Acesso negado. Faça login.")
        return token

    def home(self, request):
        """
        [GET] Carrega os dados do dashboard da API e renderiza o gráfico.
        Esperado retorno da API:
            - most_frequent_searches: lista de termos mais buscados
            - alerts: lista de componentes com estoque crítico
            - missing_searches: buscas sem resultado
        """
        token = self._get_token(request)
        if not token:
            return redirect("login:login")

        try:
            response = requests.get(
                f"{settings.API_URL}/dashboard/dashboard/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                data = response.json()
                return render(request, "dashboard/index.html", data)
            messages.error(request, f"Erro ao carregar dashboard. Código: {response.status_code}")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {e}")

        return redirect("componentes:lista")
