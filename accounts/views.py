from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileUpdateForm, RegisterForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    pass


def register_view(request):
    if request.user.is_authenticated:
        return redirect("stages:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.display_name()} ! Votre compte a été créé.")
            return redirect("stages:dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})
