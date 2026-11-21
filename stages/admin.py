from django.contrib import admin
from .models import Candidature, OffreStage, RapportSuivi, Stage


@admin.register(OffreStage)
class OffreStageAdmin(admin.ModelAdmin):
    list_display = ("titre", "entreprise", "domaine", "lieu", "duree_mois", "date_limite", "est_active")
    list_filter = ("est_active", "domaine", "lieu")
    search_fields = ("titre", "description", "entreprise__organisation", "entreprise__username")


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ("offre", "etudiant", "statut", "date_candidature", "date_decision")
    list_filter = ("statut", "date_candidature")
    search_fields = ("offre__titre", "etudiant__username", "etudiant__last_name")


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("titre", "etudiant", "entreprise", "encadreur", "statut", "note_finale")
    list_filter = ("statut", "encadreur")
    search_fields = ("titre", "etudiant__username", "entreprise__organisation")


@admin.register(RapportSuivi)
class RapportSuiviAdmin(admin.ModelAdmin):
    list_display = ("titre", "stage", "auteur", "avancement_pourcent", "statut", "date_soumission")
    list_filter = ("statut", "date_soumission")
    search_fields = ("titre", "stage__titre", "auteur__username")
