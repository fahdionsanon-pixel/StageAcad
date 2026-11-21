from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from stages.models import Candidature, OffreStage, RapportSuivi, Stage


class StageWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_test", password="password123", role=User.Role.ADMIN, is_staff=True
        )
        self.entreprise = User.objects.create_user(
            username="ent_test", password="password123", role=User.Role.ENTREPRISE, organisation="Acme Tech"
        )
        self.encadreur = User.objects.create_user(
            username="enc_test", password="password123", role=User.Role.ENCADREUR, first_name="Jean", last_name="Martin"
        )
        self.etudiant = User.objects.create_user(
            username="etu_test", password="password123", role=User.Role.ETUDIANT, first_name="Amina", last_name="Diallo"
        )
        today = timezone.localdate()
        self.offre = OffreStage.objects.create(
            titre="Stage Backend Django",
            entreprise=self.entreprise,
            domaine="Informatique",
            lieu=OffreStage.Ville.OUAGADOUGOU,
            duree_mois=3,
            date_debut=today + timedelta(days=10),
            date_limite=today + timedelta(days=30),
            description="Développement d'API et interface Django.",
        )

    def test_full_internship_lifecycle(self):
        # 1. L'étudiant postule à l'offre
        self.client.login(username="etu_test", password="password123")
        resp = self.client.post(
            reverse("stages:offre_detail", args=[self.offre.pk]),
            {"lettre_motivation": "Je suis très motivée par ce stage."},
        )
        self.assertEqual(resp.status_code, 302)
        candidature = Candidature.objects.get(offre=self.offre, etudiant=self.etudiant)
        self.assertEqual(candidature.statut, Candidature.Statut.EN_ATTENTE)

        # 2. L'entreprise accepte la candidature -> crée automatiquement le Stage
        self.client.login(username="ent_test", password="password123")
        resp = self.client.post(
            reverse("stages:candidature_decider", args=[candidature.pk, "accepter"]),
            {"commentaire_entreprise": "Bienvenue !"},
        )
        self.assertEqual(resp.status_code, 302)
        candidature.refresh_from_db()
        self.assertEqual(candidature.statut, Candidature.Statut.ACCEPTEE)
        stage = Stage.objects.get(candidature=candidature)
        self.assertEqual(stage.statut, Stage.Statut.EN_ATTENTE_ENCADREUR)
        self.assertIsNone(stage.encadreur)

        # 3. L'admin affecte un encadreur -> le stage passe EN_COURS
        self.client.login(username="admin_test", password="password123")
        resp = self.client.post(
            reverse("stages:stage_detail", args=[stage.pk]),
            {
                "action": "affecter_encadreur",
                "encadreur": self.encadreur.pk,
                "statut": Stage.Statut.EN_ATTENTE_ENCADREUR,
            },
        )
        self.assertEqual(resp.status_code, 302)
        stage.refresh_from_db()
        self.assertEqual(stage.encadreur, self.encadreur)
        self.assertEqual(stage.statut, Stage.Statut.EN_COURS)

        # 4. L'étudiant soumet un rapport de suivi
        self.client.login(username="etu_test", password="password123")
        resp = self.client.post(
            reverse("stages:stage_detail", args=[stage.pk]),
            {
                "action": "soumettre_rapport",
                "titre": "Rapport mi-parcours",
                "avancement_pourcent": 50,
                "contenu": "Première moitié terminée.",
            },
        )
        self.assertEqual(resp.status_code, 302)
        rapport = RapportSuivi.objects.get(stage=stage)
        self.assertEqual(rapport.statut, RapportSuivi.Statut.SOUMIS)

        # 5. L'encadreur valide le rapport et évalue le stage
        self.client.login(username="enc_test", password="password123")
        resp = self.client.post(
            reverse("stages:rapport_reviser", args=[rapport.pk]),
            {"statut": RapportSuivi.Statut.VALIDE, "commentaire_encadreur": "Excellent travail."},
        )
        self.assertEqual(resp.status_code, 302)
        rapport.refresh_from_db()
        self.assertEqual(rapport.statut, RapportSuivi.Statut.VALIDE)

        resp = self.client.post(
            reverse("stages:stage_detail", args=[stage.pk]),
            {
                "action": "evaluer_stage",
                "statut": Stage.Statut.TERMINE,
                "note_finale": "17.50",
                "appreciation_finale": "Très bon stage.",
            },
        )
        self.assertEqual(resp.status_code, 302)
        stage.refresh_from_db()
        self.assertEqual(stage.statut, Stage.Statut.TERMINE)
        self.assertEqual(float(stage.note_finale), 17.5)

    def test_etudiant_cannot_create_offre(self):
        self.client.login(username="etu_test", password="password123")
        resp = self.client.get(reverse("stages:offre_create"))
        self.assertEqual(resp.status_code, 403)

    def test_pages_render_for_public_and_student(self):
        self.assertEqual(self.client.get(reverse("stages:home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("stages:offre_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("accounts:login")).status_code, 200)

        self.client.login(username="etu_test", password="password123")
        self.assertEqual(self.client.get(reverse("stages:dashboard")).status_code, 200)
        self.assertEqual(self.client.get(reverse("stages:candidature_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("stages:stage_list")).status_code, 200)

