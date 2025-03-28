from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.conf import settings

API_URL = settings.API_URL


def dashboard_home(request):
    token = request.session.get("access")
    if not token:
        messages.error(request, "Acesso negado. Faça login.")
        return redirect("login:login")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{API_URL}/dashboard/dashboard/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return render(request, "dashboard/index.html", data)
        else:
            messages.error(request, "Erro ao carregar dashboard.")
    except Exception as e:
        messages.error(request, f"Erro inesperado: {e}")

    return redirect("componentes:lista")
