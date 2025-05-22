from django.urls import path
from .views import LoginView

view = LoginView()

app_name = "login"

urlpatterns = [
    path("", view.login, name="login"),
    path("logout/", view.logout, name="logout"),
    path("password-reset/", view.password_reset, name="password_reset"),
    path("password-reset-confirm/", view.password_reset_confirm, name="password_reset_confirm"),
]
