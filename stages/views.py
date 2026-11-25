from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import User
from .forms import (
    AffectationEncadreurForm,
    CandidatureForm,
    EvaluationStageForm,
    OffreStageForm,
    RapportSuiviForm,
    RevisionRapportForm,
)
from .models import Candidature, OffreStage, RapportSuivi, Stage


def home(request):
    offres_recentes = OffreStage.objects.filter(est_active=True).select_related("entreprise")[:6]
    stats = {
        "offres": OffreStage.objects.filter(est_active=True).count(),
        "entreprises": User.objects.filter(role=User.Role.ENTREPRISE).count(),
        "etudiants": User.objects.filter(role=User.Role.ETUDIANT).count(),
        "stages": Stage.objects.count(),
    }
    return render(request, "home.html", {"offres_recentes": offres_recentes, "stats": stats})


@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.is_admin_role:
        context.update(
            {
                "nb_offres": OffreStage.objects.count(),
                "nb_candidatures": Candidature.objects.count(),
                "nb_stages": Stage.objects.count(),
                "stages_sans_encadreur": Stage.objects.filter(encadreur__isnull=True).select_related(
                    "etudiant", "entreprise"
                ),
                "derniers_stages": Stage.objects.select_related("etudiant", "entreprise", "encadreur")[:5],
                "dernieres_candidatures": Candidature.objects.select_related("offre", "etudiant")[:5],
            }
        )
    elif user.is_entreprise:
        mes_offres = OffreStage.objects.filter(entreprise=user)
        candidatures_recues = Candidature.objects.filter(offre__entreprise=user).select_related("offre", "etudiant")
        mes_stages = Stage.objects.filter(entreprise=user).select_related("etudiant", "encadreur")
        context.update(
            {
                "nb_offres": mes_offres.count(),
                "nb_candidatures_attente": candidatures_recues.filter(statut=Candidature.Statut.EN_ATTENTE).count(),
                "nb_stages": mes_stages.count(),
                "mes_offres": mes_offres[:5],
                "candidatures_recues": candidatures_recues[:6],
            }
        )
    elif user.is_encadreur:
        stages_encadres = Stage.objects.filter(encadreur=user).select_related("etudiant", "entreprise")
        rapports_attente = RapportSuivi.objects.filter(
            stage__encadreur=user, statut=RapportSuivi.Statut.SOUMIS
        ).select_related("stage", "auteur")
        context.update(
            {
                "nb_stages": stages_encadres.count(),
                "nb_rapports_attente": rapports_attente.count(),
                "stages_encadres": stages_encadres,
                "rapports_attente": rapports_attente[:6],
            }
        )
    else:  # Étudiant
        mes_candidatures = Candidature.objects.filter(etudiant=user).select_related("offre", "offre__entreprise")
        mes_stages = Stage.objects.filter(etudiant=user).select_related("entreprise", "encadreur", "candidature")
        offres_actives = OffreStage.objects.filter(est_active=True).select_related("entreprise")[:4]

        stage_actif = mes_stages.first()
        derniere_cand = mes_candidatures.first()

        # Calcul dynamique des 5 étapes du suivi de dossier
        step1_done = mes_candidatures.exists() or stage_actif is not None
        step2_done = stage_actif is not None or mes_candidatures.filter(statut=Candidature.Statut.ACCEPTEE).exists()
        step3_done = bool(stage_actif and stage_actif.encadreur_id)
        rapports_stage = stage_actif.rapports.all() if stage_actif else RapportSuivi.objects.none()
        nb_rapports = rapports_stage.count()
        step4_done = bool(stage_actif and (stage_actif.statut == Stage.Statut.TERMINE or rapports_stage.filter(statut=RapportSuivi.Statut.VALIDE).exists() and stage_actif.note_finale is not None))
        step5_done = bool(stage_actif and (stage_actif.statut == Stage.Statut.TERMINE or stage_actif.note_finale is not None))

        etapes_validees = sum([step1_done, step2_done, step3_done, step4_done, step5_done])
        # Circonférence SVG pour r=34 : 2 * pi * 34 ≈ 213.6
        ring_circumference = 213.6
        ring_offset = round(ring_circumference * (1 - etapes_validees / 5), 1)

        # Détermination de l'étape active (en cours)
        if not step1_done:
            current_step = 1
        elif not step2_done:
            current_step = 2
        elif not step3_done:
            current_step = 3
        elif not step5_done:
            current_step = 4
        else:
            current_step = 5

        cand_origine = stage_actif.candidature if (stage_actif and stage_actif.candidature) else derniere_cand
        etapes = [
            {
                "num": 1,
                "label": "Candidature",
                "done": step1_done,
                "current": current_step == 1,
                "meta": cand_origine.date_candidature.strftime("%d %b") if cand_origine else "À faire",
            },
            {
                "num": 2,
                "label": "Acceptée",
                "done": step2_done,
                "current": current_step == 2,
                "meta": (
                    cand_origine.date_decision.strftime("%d %b")
                    if (cand_origine and cand_origine.date_decision)
                    else ("Validée" if step2_done else "En attente")
                ),
            },
            {
                "num": 3,
                "label": "Encadreur",
                "done": step3_done,
                "current": current_step == 3,
                "meta": stage_actif.date_creation.strftime("%d %b") if step3_done else "En attente",
            },
            {
                "num": 4,
                "label": "Rapports",
                "done": step4_done,
                "current": current_step == 4,
                "meta": f"{nb_rapports} déposé(s)" if nb_rapports else ("en cours" if step3_done else "À venir"),
            },
            {
                "num": 5,
                "label": "Évaluation",
                "done": step5_done,
                "current": current_step == 5 and not step5_done,
                "meta": (
                    f"{stage_actif.note_finale}/20"
                    if (stage_actif and stage_actif.note_finale is not None)
                    else (stage_actif.date_fin.strftime("%b %Y") if stage_actif else "À venir")
                ),
            },
        ]

        # Prochaines échéances
        echeances = []
        if stage_actif:
            rapport_a_corriger = rapports_stage.filter(statut=RapportSuivi.Statut.A_CORRIGER).first()
            if rapport_a_corriger:
                echeances.append(
                    {
                        "jour": rapport_a_corriger.date_soumission.strftime("%d"),
                        "mois": rapport_a_corriger.date_soumission.strftime("%b").lower(),
                        "titre": f"Corriger : {rapport_a_corriger.titre}",
                        "sous_titre": "Modifications demandées par l'encadreur",
                        "badge": "À corriger",
                        "badge_class": "bg-red-50 text-red-700",
                    }
                )
            echeances.append(
                {
                    "jour": stage_actif.date_debut.strftime("%d"),
                    "mois": stage_actif.date_debut.strftime("%b").lower(),
                    "titre": f"Rapport n°{nb_rapports + 1}",
                    "sous_titre": "À déposer en ligne dans le suivi",
                    "badge": "À faire",
                    "badge_class": "bg-amber-50 text-amber-700",
                }
            )
            echeances.append(
                {
                    "jour": stage_actif.date_fin.strftime("%d"),
                    "mois": stage_actif.date_fin.strftime("%b").lower(),
                    "titre": "Fin de stage & Évaluation",
                    "sous_titre": f"{stage_actif.entreprise.display_name()}",
                    "badge": "Terminé" if step5_done else "À venir",
                    "badge_class": "bg-emerald-50 text-emerald-700" if step5_done else "bg-blue-50 text-blue-700",
                }
            )
        else:
            echeances.append(
                {
                    "jour": timezone.localdate().strftime("%d"),
                    "mois": timezone.localdate().strftime("%b").lower(),
                    "titre": "Postuler à une offre de stage",
                    "sous_titre": "Consultez les offres ouvertes et déposez votre CV",
                    "badge": "À faire",
                    "badge_class": "bg-amber-50 text-amber-700",
                }
            )

        context.update(
            {
                "nb_candidatures": mes_candidatures.count(),
                "nb_stages": mes_stages.count(),
                "mes_candidatures": mes_candidatures[:5],
                "mes_stages": mes_stages,
                "offres_actives": offres_actives,
                "stage_actif": stage_actif,
                "etapes": etapes,
                "etapes_validees": etapes_validees,
                "ring_offset": ring_offset,
                "echeances": echeances,
                "prochain_rapport_num": nb_rapports + 1,
            }
        )

    return render(request, "stages/dashboard.html", context)


def offre_list(request):
    offres = OffreStage.objects.select_related("entreprise")
    if request.user.is_authenticated and request.user.is_admin_role:
        pass
    elif request.user.is_authenticated and request.user.is_entreprise:
        offres = offres.filter(Q(est_active=True) | Q(entreprise=request.user))
    else:
        offres = offres.filter(est_active=True)

    q = request.GET.get("q", "").strip()
    domaine = request.GET.get("domaine", "").strip()
    lieu = request.GET.get("lieu", "").strip()

    if q:
        offres = offres.filter(
            Q(titre__icontains=q)
            | Q(description__icontains=q)
            | Q(competences_requises__icontains=q)
            | Q(entreprise__organisation__icontains=q)
        )
    if domaine:
        offres = offres.filter(domaine__icontains=domaine)
    if lieu:
        offres = offres.filter(lieu__icontains=lieu)

    domaines = OffreStage.objects.values_list("domaine", flat=True).distinct().order_by("domaine")
    villes = OffreStage.Ville.choices
    return render(
        request,
        "stages/offre_list.html",
        {"offres": offres, "domaines": domaines, "villes": villes, "q": q, "domaine": domaine, "lieu": lieu},
    )


def offre_detail(request, pk):
    offre = get_object_or_404(OffreStage.objects.select_related("entreprise"), pk=pk)
    deja_postule = None
    stage_en_cours = None
    form = None

    if request.user.is_authenticated and request.user.is_etudiant:
        deja_postule = Candidature.objects.filter(offre=offre, etudiant=request.user).first()
        stage_en_cours = Stage.objects.filter(
            etudiant=request.user,
            statut__in=[Stage.Statut.EN_ATTENTE_ENCADREUR, Stage.Statut.EN_COURS],
        ).first()

        if not deja_postule and offre.est_ouverte:
            if stage_en_cours:
                if request.method == "POST":
                    messages.error(
                        request,
                        "Vous avez déjà un stage en cours. Vous ne pouvez pas déposer une nouvelle candidature avant la fin de ce stage.",
                    )
                    return redirect("stages:offre_detail", pk=offre.pk)
            else:
                if request.method == "POST":
                    form = CandidatureForm(request.POST, request.FILES)
                    if form.is_valid():
                        candidature = form.save(commit=False)
                        candidature.offre = offre
                        candidature.etudiant = request.user
                        candidature.save()
                        messages.success(request, "Votre candidature a été envoyée avec succès.")
                        return redirect("stages:offre_detail", pk=offre.pk)
                else:
                    form = CandidatureForm()

    peut_gerer = request.user.is_authenticated and (
        request.user.is_admin_role or offre.entreprise_id == request.user.id
    )
    candidatures = offre.candidatures.select_related("etudiant") if peut_gerer else None

    return render(
        request,
        "stages/offre_detail.html",
        {
            "offre": offre,
            "deja_postule": deja_postule,
            "stage_en_cours": stage_en_cours,
            "form": form,
            "peut_gerer": peut_gerer,
            "candidatures": candidatures,
        },
    )


@login_required
def offre_create(request):
    if not (request.user.is_entreprise or request.user.is_admin_role):
        raise PermissionDenied("Seules les entreprises ou l'administrateur peuvent publier une offre.")

    if request.method == "POST":
        form = OffreStageForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise = request.user
            offre.save()
            messages.success(request, "L'offre de stage a été publiée.")
            return redirect("stages:offre_detail", pk=offre.pk)
    else:
        form = OffreStageForm()

    return render(request, "stages/offre_form.html", {"form": form, "titre_page": "Publier une offre de stage"})


@login_required
def offre_edit(request, pk):
    offre = get_object_or_404(OffreStage, pk=pk)
    if not (request.user.is_admin_role or offre.entreprise_id == request.user.id):
        raise PermissionDenied("Vous ne pouvez pas modifier cette offre.")

    if request.method == "POST":
        form = OffreStageForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            messages.success(request, "L'offre de stage a été mise à jour.")
            return redirect("stages:offre_detail", pk=offre.pk)
    else:
        form = OffreStageForm(instance=offre)

    return render(request, "stages/offre_form.html", {"form": form, "offre": offre, "titre_page": "Modifier l'offre"})


@login_required
def offre_delete(request, pk):
    offre = get_object_or_404(OffreStage, pk=pk)
    if not (request.user.is_admin_role or offre.entreprise_id == request.user.id):
        raise PermissionDenied("Vous ne pouvez pas supprimer cette offre.")

    if request.method == "POST":
        offre.delete()
        messages.success(request, "L'offre de stage a été supprimée.")
        return redirect("stages:offre_list")

    return redirect("stages:offre_detail", pk=pk)


@login_required
def candidature_list(request):
    user = request.user
    if user.is_admin_role:
        candidatures = Candidature.objects.select_related("offre", "offre__entreprise", "etudiant")
    elif user.is_entreprise:
        candidatures = Candidature.objects.filter(offre__entreprise=user).select_related("offre", "etudiant")
    elif user.is_etudiant:
        candidatures = Candidature.objects.filter(etudiant=user).select_related("offre", "offre__entreprise")
    else:
        raise PermissionDenied("Accès réservé aux étudiants, entreprises et administrateurs.")

    statut = request.GET.get("statut", "").strip()
    counts = {
        "all": candidatures.count(),
        "EN_ATTENTE": candidatures.filter(statut=Candidature.Statut.EN_ATTENTE).count(),
        "ACCEPTEE": candidatures.filter(statut=Candidature.Statut.ACCEPTEE).count(),
        "REFUSEE": candidatures.filter(statut=Candidature.Statut.REFUSEE).count(),
    }
    if statut:
        candidatures = candidatures.filter(statut=statut)

    return render(
        request,
        "stages/candidature_list.html",
        {
            "candidatures": candidatures,
            "statut_filtre": statut,
            "statuts": Candidature.Statut.choices,
            "counts": counts,
        },
    )


@login_required
def candidature_decider(request, pk, decision):
    candidature = get_object_or_404(Candidature.objects.select_related("offre", "etudiant"), pk=pk)
    if not (request.user.is_admin_role or candidature.offre.entreprise_id == request.user.id):
        raise PermissionDenied("Action non autorisée.")

    if request.method == "POST":
        commentaire = request.POST.get("commentaire_entreprise", "").strip()
        if decision == "accepter":
            stage = candidature.accepter(commentaire=commentaire)
            messages.success(
                request,
                f"Candidature de {candidature.etudiant.display_name()} acceptée ! "
                f"Le stage « {stage.titre} » a été créé et attend l'affectation d'un encadreur.",
            )
        elif decision == "refuser":
            candidature.refuser(commentaire=commentaire)
            messages.info(request, f"Candidature de {candidature.etudiant.display_name()} refusée.")

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("stages:candidature_list")


@login_required
def stage_list(request):
    user = request.user
    if user.is_admin_role:
        stages = Stage.objects.select_related("etudiant", "entreprise", "encadreur")
    elif user.is_encadreur:
        stages = Stage.objects.filter(encadreur=user).select_related("etudiant", "entreprise", "encadreur")
    elif user.is_entreprise:
        stages = Stage.objects.filter(entreprise=user).select_related("etudiant", "entreprise", "encadreur")
    else:
        stages = Stage.objects.filter(etudiant=user).select_related("etudiant", "entreprise", "encadreur")

    statut = request.GET.get("statut", "").strip()
    if statut:
        stages = stages.filter(statut=statut)

    encadreurs = User.objects.filter(role=User.Role.ENCADREUR, is_active=True).order_by("last_name", "first_name")
    return render(
        request,
        "stages/stage_list.html",
        {
            "stages": stages,
            "statut_filtre": statut,
            "statuts": Stage.Statut.choices,
            "encadreurs": encadreurs,
        },
    )


@login_required
def stage_detail(request, pk):
    stage = get_object_or_404(Stage.objects.select_related("etudiant", "entreprise", "encadreur"), pk=pk)
    user = request.user
    if not (
        user.is_admin_role
        or stage.etudiant_id == user.id
        or stage.entreprise_id == user.id
        or stage.encadreur_id == user.id
    ):
        raise PermissionDenied("Vous n'avez pas accès à ce stage.")

    affectation_form = AffectationEncadreurForm(instance=stage) if user.is_admin_role else None
    evaluation_form = (
        EvaluationStageForm(instance=stage) if (user.is_admin_role or stage.encadreur_id == user.id) else None
    )
    rapport_form = RapportSuiviForm() if stage.etudiant_id == user.id else None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "affecter_encadreur" and user.is_admin_role:
            affectation_form = AffectationEncadreurForm(request.POST, instance=stage)
            if affectation_form.is_valid():
                updated = affectation_form.save(commit=False)
                if updated.encadreur and updated.statut == Stage.Statut.EN_ATTENTE_ENCADREUR:
                    updated.statut = Stage.Statut.EN_COURS
                updated.save()
                messages.success(request, "L'affectation de l'encadreur a été enregistrée.")
                return redirect("stages:stage_detail", pk=stage.pk)

        elif action == "evaluer_stage" and (user.is_admin_role or stage.encadreur_id == user.id):
            evaluation_form = EvaluationStageForm(request.POST, instance=stage)
            if evaluation_form.is_valid():
                evaluation_form.save()
                messages.success(request, "L'évaluation du stage a été mise à jour.")
                return redirect("stages:stage_detail", pk=stage.pk)

        elif action == "soumettre_rapport" and stage.etudiant_id == user.id:
            rapport_form = RapportSuiviForm(request.POST, request.FILES)
            if rapport_form.is_valid():
                rapport = rapport_form.save(commit=False)
                rapport.stage = stage
                rapport.auteur = user
                rapport.save()
                messages.success(request, "Votre rapport de suivi a été soumis.")
                return redirect("stages:stage_detail", pk=stage.pk)

    rapports = stage.rapports.select_related("auteur")
    peut_reviser = user.is_admin_role or stage.encadreur_id == user.id

    return render(
        request,
        "stages/stage_detail.html",
        {
            "stage": stage,
            "rapports": rapports,
            "affectation_form": affectation_form,
            "evaluation_form": evaluation_form,
            "rapport_form": rapport_form,
            "peut_reviser": peut_reviser,
            "revision_form": RevisionRapportForm(),
        },
    )


@login_required
def rapport_reviser(request, pk):
    rapport = get_object_or_404(RapportSuivi.objects.select_related("stage"), pk=pk)
    user = request.user
    if not (user.is_admin_role or rapport.stage.encadreur_id == user.id):
        raise PermissionDenied("Seul l'encadreur affecté ou l'administrateur peut réviser ce rapport.")

    if request.method == "POST":
        form = RevisionRapportForm(request.POST, instance=rapport)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.date_revision = timezone.now()
            rev.save()
            messages.success(request, f"Le rapport « {rev.titre} » a été mis à jour ({rev.get_statut_display()}).")

    return redirect("stages:stage_detail", pk=rapport.stage_id)
