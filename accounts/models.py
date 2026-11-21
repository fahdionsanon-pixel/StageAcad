from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ETUDIANT = "ETUDIANT", "Étudiant"
        ENTREPRISE = "ENTREPRISE", "Entreprise"
        ENCADREUR = "ENCADREUR", "Encadreur académique"
        ADMIN = "ADMIN", "Administrateur"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ETUDIANT,
        verbose_name="Rôle",
    )
    telephone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    # Champs spécifiques selon le rôle
    organisation = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Entreprise / Établissement",
    )
    filiere = models.CharField(max_length=120, blank=True, verbose_name="Filière / Département")
    niveau = models.CharField(max_length=60, blank=True, verbose_name="Niveau d'études")
    specialite = models.CharField(max_length=120, blank=True, verbose_name="Spécialité")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    @property
    def is_etudiant(self) -> bool:
        return self.role == self.Role.ETUDIANT

    @property
    def is_entreprise(self) -> bool:
        return self.role == self.Role.ENTREPRISE

    @property
    def is_encadreur(self) -> bool:
        return self.role == self.Role.ENCADREUR

    @property
    def is_admin_role(self) -> bool:
        return self.role == self.Role.ADMIN or self.is_superuser

    def display_name(self) -> str:
        if self.is_entreprise and self.organisation:
            return self.organisation
        full = self.get_full_name().strip()
        return full if full else self.username

    @property
    def initials(self) -> str:
        name = self.display_name().strip()
        parts = [p for p in name.replace(".", " ").split() if p]
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return name[:2].upper() if name else "US"

    def __str__(self) -> str:
        return f"{self.display_name()} ({self.get_role_display()})"
