from django.urls import path
from . import views

app_name = "stages"

urlpatterns = [
    path("", views.home, name="home"),
    path("tableau-de-bord/", views.dashboard, name="dashboard"),
    # Offres de stage
    path("offres/", views.offre_list, name="offre_list"),
    path("offres/nouvelle/", views.offre_create, name="offre_create"),
    path("offres/<int:pk>/", views.offre_detail, name="offre_detail"),
    path("offres/<int:pk>/modifier/", views.offre_edit, name="offre_edit"),
    path("offres/<int:pk>/supprimer/", views.offre_delete, name="offre_delete"),
    # Candidatures
    path("candidatures/", views.candidature_list, name="candidature_list"),
    path("candidatures/<int:pk>/<str:decision>/", views.candidature_decider, name="candidature_decider"),
    # Stages & affectation des encadreurs & suivi
    path("stages/", views.stage_list, name="stage_list"),
    path("stages/<int:pk>/", views.stage_detail, name="stage_detail"),
    path("rapports/<int:pk>/reviser/", views.rapport_reviser, name="rapport_reviser"),
]
