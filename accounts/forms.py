from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

INPUT_CLASS = (
    "w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 "
    "shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
)


class RegisterForm(UserCreationForm):
    PUBLIC_ROLES = [
        (User.Role.ETUDIANT, "Étudiant"),
        (User.Role.ENTREPRISE, "Entreprise"),
        (User.Role.ENCADREUR, "Encadreur académique"),
    ]

    role = forms.ChoiceField(
        choices=PUBLIC_ROLES,
        label="Type de compte",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "telephone",
            "organisation",
            "filiere",
            "niveau",
            "specialite",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "role":
                field.widget.attrs["class"] = INPUT_CLASS
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["organisation"].help_text = "Obligatoire pour une entreprise ; facultatif sinon."


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "telephone", "organisation", "filiere", "niveau", "specialite")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS
