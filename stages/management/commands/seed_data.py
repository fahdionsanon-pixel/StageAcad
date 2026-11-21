from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from stages.models import Candidature, OffreStage, RapportSuivi, Stage


class Command(BaseCommand):
    help = "Peuple la base de données avec des données de démonstration réalistes."

    def handle(self, *args, **options):
        today = timezone.localdate()

        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "Nadia",
                "last_name": "Benali",
                "email": "admin@univ-stages.edu",
                "role": User.Role.ADMIN,
                "organisation": "Service des Stages Académiques",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("admin123")
        admin_user.save()

        ent1, _ = User.objects.get_or_create(
            username="techvision",
            defaults={
                "first_name": "Marc",
                "last_name": "Laurent",
                "email": "rh@techvision.fr",
                "role": User.Role.ENTREPRISE,
                "organisation": "TechVision Solutions",
                "telephone": "+33 1 42 68 50 10",
            },
        )
        ent1.set_password("demo1234")
        ent1.save()

        ent2, _ = User.objects.get_or_create(
            username="datanexus",
            defaults={
                "first_name": "Sophie",
                "last_name": "Mercier",
                "email": "stages@datanexus.io",
                "role": User.Role.ENTREPRISE,
                "organisation": "DataNexus Analytics",
                "telephone": "+33 4 72 10 22 33",
            },
        )
        ent2.set_password("demo1234")
        ent2.save()

        enc1, _ = User.objects.get_or_create(
            username="prof_dupont",
            defaults={
                "first_name": "Dr. Jean",
                "last_name": "Dupont",
                "email": "j.dupont@univ-stages.edu",
                "role": User.Role.ENCADREUR,
                "filiere": "Informatique & Génie Logiciel",
                "specialite": "Architecture Web & Cloud",
            },
        )
        enc1.set_password("demo1234")
        enc1.save()

        enc2, _ = User.objects.get_or_create(
            username="prof_kone",
            defaults={
                "first_name": "Pr. Aminata",
                "last_name": "Koné",
                "email": "a.kone@univ-stages.edu",
                "role": User.Role.ENCADREUR,
                "filiere": "Data Science & IA",
                "specialite": "Machine Learning appliqué",
            },
        )
        enc2.set_password("demo1234")
        enc2.save()

        etu1, _ = User.objects.get_or_create(
            username="etudiant1",
            defaults={
                "first_name": "Youssef",
                "last_name": "El Amrani",
                "email": "y.elamrani@etu.univ-stages.edu",
                "role": User.Role.ETUDIANT,
                "filiere": "Génie Logiciel",
                "niveau": "Master 2",
            },
        )
        etu1.set_password("demo1234")
        etu1.save()

        etu2, _ = User.objects.get_or_create(
            username="etudiant2",
            defaults={
                "first_name": "Claire",
                "last_name": "Moreau",
                "email": "c.moreau@etu.univ-stages.edu",
                "role": User.Role.ETUDIANT,
                "filiere": "Data Science",
                "niveau": "Master 1",
            },
        )
        etu2.set_password("demo1234")
        etu2.save()

        etu3, _ = User.objects.get_or_create(
            username="etudiant3",
            defaults={
                "first_name": "Lucas",
                "last_name": "Bernard",
                "email": "l.bernard@etu.univ-stages.edu",
                "role": User.Role.ETUDIANT,
                "filiere": "Cybersécurité",
                "niveau": "Licence 3",
            },
        )
        etu3.set_password("demo1234")
        etu3.save()

        offres_data = [
            {
                "titre": "Développeur Web Full-Stack Django / Python",
                "entreprise": ent1,
                "domaine": "Développement Web",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=20),
                "date_limite": today + timedelta(days=45),
                "description": (
                    "Vous intégrerez l'équipe produit pour concevoir et développer de nouvelles fonctionnalités "
                    "sur notre plateforme SaaS en Django, PostgreSQL et Tailwind CSS."
                ),
                "competences_requises": "Python, Django, HTML/CSS, Git, bases de données relationnelles.",
            },
            {
                "titre": "Stage Data Analyst & Visualisation BI",
                "entreprise": ent2,
                "domaine": "Data & IA",
                "lieu": OffreStage.Ville.BOBO_DIOULASSO,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=30),
                "date_limite": today + timedelta(days=60),
                "description": (
                    "Analyse des indicateurs de performance clients, création de tableaux de bord automatisés "
                    "et nettoyage de pipelines de données."
                ),
                "competences_requises": "Python, Pandas, SQL, Power BI ou Tableau.",
            },
            {
                "titre": "Ingénieur DevOps & CI/CD Junior",
                "entreprise": ent1,
                "domaine": "Cloud & DevOps",
                "lieu": OffreStage.Ville.ABIDJAN,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=15),
                "date_limite": today + timedelta(days=40),
                "description": (
                    "Automatisation des déploiements Docker, mise en place de pipelines GitHub Actions "
                    "et monitoring d'applications web."
                ),
                "competences_requises": "Linux, Docker, GitHub Actions, notions de cloud.",
            },
            {
                "titre": "Stage Machine Learning — Détection d'anomalies",
                "entreprise": ent2,
                "domaine": "Data & IA",
                "lieu": OffreStage.Ville.DAKAR,
                "duree_mois": 6,
                "date_debut": today + timedelta(days=25),
                "date_limite": today + timedelta(days=50),
                "description": (
                    "Prototypage et évaluation de modèles supervisés et non supervisés pour détecter "
                    "les anomalies sur des flux temporels."
                ),
                "competences_requises": "Python, Scikit-learn, statistiques, Jupyter.",
            },
        ]

        offres = []
        for data in offres_data:
            offre, _ = OffreStage.objects.get_or_create(
                titre=data["titre"], entreprise=data["entreprise"], defaults=data
            )
            offres.append(offre)

        # Candidature acceptée -> Stage en cours avec encadreur + rapports
        cand1, created1 = Candidature.objects.get_or_create(
            offre=offres[0],
            etudiant=etu1,
            defaults={
                "lettre_motivation": (
                    "Étudiant en Master 2 Génie Logiciel, je maîtrise Django et je souhaite mettre mes compétences "
                    "au service de TechVision Solutions."
                ),
            },
        )
        if created1 or cand1.statut == Candidature.Statut.EN_ATTENTE:
            stage1 = cand1.accepter(commentaire="Excellent profil technique, bienvenue dans l'équipe !")
            stage1.encadreur = enc1
            stage1.statut = Stage.Statut.EN_COURS
            stage1.save()

            RapportSuivi.objects.get_or_create(
                stage=stage1,
                titre="Semaine 1-2 : Prise en main de l'architecture",
                defaults={
                    "auteur": etu1,
                    "contenu": (
                        "Installation de l'environnement, revue du modèle de données et mise en place des premiers "
                        "tests unitaires sur le module d'authentification."
                    ),
                    "avancement_pourcent": 25,
                    "statut": RapportSuivi.Statut.VALIDE,
                    "commentaire_encadreur": "Très bon démarrage, pensez à documenter le schéma relationnel.",
                    "date_revision": timezone.now(),
                },
            )
            RapportSuivi.objects.get_or_create(
                stage=stage1,
                titre="Semaine 3-4 : Module de gestion des candidatures",
                defaults={
                    "auteur": etu1,
                    "contenu": (
                        "Implémentation des vues de filtrage, formulaires de candidature avec upload de CV "
                        "et notifications de statut."
                    ),
                    "avancement_pourcent": 50,
                    "statut": RapportSuivi.Statut.SOUMIS,
                },
            )

        # Candidature acceptée en attente d'affectation d'encadreur
        cand2, created2 = Candidature.objects.get_or_create(
            offre=offres[1],
            etudiant=etu2,
            defaults={
                "lettre_motivation": "Passionnée par la data visualisation et Python, je candidate pour ce stage BI.",
            },
        )
        if created2 or cand2.statut == Candidature.Statut.EN_ATTENTE:
            cand2.accepter(commentaire="Profil retenu après entretien.")

        # Candidature en attente
        Candidature.objects.get_or_create(
            offre=offres[2],
            etudiant=etu3,
            defaults={
                "lettre_motivation": "Je souhaite approfondir mes compétences en Docker et CI/CD au sein de votre équipe.",
            },
        )

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès !"))
        self.stdout.write("Comptes de test :")
        self.stdout.write("  - Admin      : admin / admin123")
        self.stdout.write("  - Entreprise : techvision / demo1234  (ou datanexus / demo1234)")
        self.stdout.write("  - Encadreur  : prof_dupont / demo1234 (ou prof_kone / demo1234)")
        self.stdout.write("  - Étudiant   : etudiant1 / demo1234   (ou etudiant2, etudiant3 / demo1234)")
