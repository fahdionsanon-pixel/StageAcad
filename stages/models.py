from datetime import timedelta
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class OffreStage(models.Model):
    class Ville(models.TextChoices):
        OUAGADOUGOU = "Ouagadougou", "Ouagadougou"
        BOBO_DIOULASSO = "Bobo-Dioulasso", "Bobo-Dioulasso"
        ABIDJAN = "Abidjan", "Abidjan"
        DAKAR = "Dakar", "Dakar"
        BAMAKO = "Bamako", "Bamako"
        LOME = "Lomé", "Lomé"
        COTONOU = "Cotonou", "Cotonou"
        NIAMEY = "Niamey", "Niamey"
        TELETRAVAIL = "Télétravail", "Télétravail"

    titre = models.CharField(max_length=200, verbose_name="Intitulé du stage")
    entreprise = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offres_publiees",
        verbose_name="Entreprise",
    )
    domaine = models.CharField(max_length=120, verbose_name="Domaine")
    lieu = models.CharField(
        max_length=150,
        choices=Ville.choices,
        default=Ville.OUAGADOUGOU,
        verbose_name="Ville du stage",
    )
    duree_mois = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(24)],
        verbose_name="Durée (mois)",
    )
    date_debut = models.DateField(verbose_name="Date de début souhaitée")
    date_limite = models.DateField(verbose_name="Date limite de candidature")
    description = models.TextField(verbose_name="Description des missions")
    competences_requises = models.TextField(blank=True, verbose_name="Compétences requises")
    est_active = models.BooleanField(default=True, verbose_name="Offre active")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Publiée le")

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Offre de stage"
        verbose_name_plural = "Offres de stage"

    @property
    def est_ouverte(self) -> bool:
        return self.est_active and self.date_limite >= timezone.localdate()

    def __str__(self) -> str:
        return f"{self.titre} — {self.entreprise.display_name()}"


class Candidature(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        ACCEPTEE = "ACCEPTEE", "Acceptée"
        REFUSEE = "REFUSEE", "Refusée"

    offre = models.ForeignKey(
        OffreStage,
        on_delete=models.CASCADE,
        related_name="candidatures",
        verbose_name="Offre de stage",
    )
    etudiant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidatures",
        verbose_name="Étudiant",
    )
    lettre_motivation = models.TextField(verbose_name="Lettre de motivation")
    cv = models.FileField(upload_to="cvs/%Y/%m/", blank=True, null=True, verbose_name="CV (PDF)")
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
        verbose_name="Statut",
    )
    commentaire_entreprise = models.TextField(blank=True, verbose_name="Commentaire de l'entreprise")
    date_candidature = models.DateTimeField(auto_now_add=True, verbose_name="Date de candidature")
    date_decision = models.DateTimeField(blank=True, null=True, verbose_name="Date de décision")

    class Meta:
        ordering = ["-date_candidature"]
        unique_together = ("offre", "etudiant")
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def accepter(self, commentaire: str = ""):
        self.statut = self.Statut.ACCEPTEE
        self.commentaire_entreprise = commentaire
        self.date_decision = timezone.now()
        self.save()
        # Crée automatiquement le stage académique associé s'il n'existe pas encore
        stage, _ = Stage.objects.get_or_create(
            candidature=self,
            defaults={
                "etudiant": self.etudiant,
                "entreprise": self.offre.entreprise,
                "titre": self.offre.titre,
                "description": self.offre.description,
                "date_debut": self.offre.date_debut,
                "date_fin": self.offre.date_debut + timedelta(days=30 * self.offre.duree_mois),
                "statut": Stage.Statut.EN_ATTENTE_ENCADREUR,
            },
        )
        return stage

    def refuser(self, commentaire: str = ""):
        self.statut = self.Statut.REFUSEE
        self.commentaire_entreprise = commentaire
        self.date_decision = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f"{self.etudiant.display_name()} → {self.offre.titre}"


class Stage(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE_ENCADREUR = "EN_ATTENTE_ENCADREUR", "En attente d'encadreur"
        EN_COURS = "EN_COURS", "En cours"
        TERMINE = "TERMINE", "Terminé"
        ANNULE = "ANNULE", "Annulé"

    candidature = models.OneToOneField(
        Candidature,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stage",
        verbose_name="Candidature d'origine",
    )
    etudiant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stages_etudiant",
        verbose_name="Étudiant stagiaire",
    )
    entreprise = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stages_entreprise",
        verbose_name="Entreprise d'accueil",
    )
    encadreur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stages_encadres",
        verbose_name="Encadreur académique",
    )
    titre = models.CharField(max_length=200, verbose_name="Sujet du stage")
    description = models.TextField(blank=True, verbose_name="Description")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    statut = models.CharField(
        max_length=25,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE_ENCADREUR,
        verbose_name="Statut",
    )
    note_finale = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Note finale (/20)",
    )
    appreciation_finale = models.TextField(blank=True, verbose_name="Appréciation finale")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    @property
    def dernier_avancement(self) -> int:
        dernier = self.rapports.order_by("-date_soumission").first()
        return dernier.avancement_pourcent if dernier else 0

    def __str__(self) -> str:
        return f"{self.titre} — {self.etudiant.display_name()}"


class RapportSuivi(models.Model):
    class Statut(models.TextChoices):
        SOUMIS = "SOUMIS", "Soumis"
        VALIDE = "VALIDE", "Validé"
        A_CORRIGER = "A_CORRIGER", "À corriger"

    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name="rapports",
        verbose_name="Stage",
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rapports_soumis",
        verbose_name="Auteur",
    )
    titre = models.CharField(max_length=200, verbose_name="Titre du point de suivi / rapport")
    contenu = models.TextField(verbose_name="Compte-rendu des activités")
    document = models.FileField(
        upload_to="rapports/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Document joint (PDF, DOCX)",
    )
    avancement_pourcent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Avancement (%)",
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.SOUMIS,
        verbose_name="Statut de validation",
    )
    commentaire_encadreur = models.TextField(blank=True, verbose_name="Commentaire de l'encadreur")
    date_soumission = models.DateTimeField(auto_now_add=True, verbose_name="Soumis le")
    date_revision = models.DateTimeField(blank=True, null=True, verbose_name="Révisé le")

    class Meta:
        ordering = ["-date_soumission"]
        verbose_name = "Rapport de suivi"
        verbose_name_plural = "Rapports de suivi"

    def __str__(self) -> str:
        return f"{self.titre} ({self.stage.etudiant.display_name()})"
