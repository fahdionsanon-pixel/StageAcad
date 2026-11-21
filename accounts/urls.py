from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.CustomLoginView.as_view(), name="login"),
    path("deconnexion/", views.CustomLogoutView.as_view(), name="logout"),
    path("inscription/", views.register_view, name="register"),
    path("profil/", views.profile_view, name="profile"),
]
