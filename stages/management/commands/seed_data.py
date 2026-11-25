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
                "email": "nadiabenali@gmail.com",
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
                "email": "marclaurent@gmail.com",
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
                "email": "sophiemercier@gmail.com",
                "role": User.Role.ENTREPRISE,
                "organisation": "DataNexus Analytics",
                "telephone": "+33 4 72 10 22 33",
            },
        )
        ent2.set_password("demo1234")
        ent2.save()

        ent3, _ = User.objects.get_or_create(
            username="fasofinance",
            defaults={
                "first_name": "Ibrahim",
                "last_name": "Ouédraogo",
                "email": "ibrahimouedraogo@gmail.com",
                "role": User.Role.ENTREPRISE,
                "organisation": "Faso Finance & Conseil",
                "telephone": "+226 25 30 44 12",
            },
        )
        ent3.set_password("demo1234")
        ent3.save()

        ent4, _ = User.objects.get_or_create(
            username="sahelbtp",
            defaults={
                "first_name": "Amadou",
                "last_name": "Traoré",
                "email": "amadoutraore@gmail.com",
                "role": User.Role.ENTREPRISE,
                "organisation": "Sahel BTP & Ingénierie",
                "telephone": "+226 20 97 18 45",
            },
        )
        ent4.set_password("demo1234")
        ent4.save()

        ent5, _ = User.objects.get_or_create(
            username="agrisol",
            defaults={
                "first_name": "Fatou",
                "last_name": "Diop",
                "email": "fatoudiop@gmail.com",
                "role": User.Role.ENTREPRISE,
                "organisation": "AgriSol Afrique",
                "telephone": "+221 33 821 40 90",
            },
        )
        ent5.set_password("demo1234")
        ent5.save()

        enc1, _ = User.objects.get_or_create(
            username="prof_dupont",
            defaults={
                "first_name": "Dr. Jean",
                "last_name": "Dupont",
                "email": "jeandupont@gmail.com",
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
                "email": "aminatakone@gmail.com",
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
                "email": "youssefelamrani@gmail.com",
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
                "email": "clairemoreau@gmail.com",
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
                "email": "lucasbernard@gmail.com",
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
            {
                "titre": "Assistant Comptable & Audit Financier",
                "entreprise": ent3,
                "domaine": "Finance & Comptabilité",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=15),
                "date_limite": today + timedelta(days=45),
                "description": (
                    "Participation à la tenue comptable, rapprochements bancaires, préparation des déclarations "
                    "fiscales et appui aux missions d'audit interne auprès des PME clientes."
                ),
                "competences_requises": "Comptabilité SYSCOHADA, Excel avancé, rigueur et confidentialité.",
            },
            {
                "titre": "Chargé de Communication Digitale & Réseaux Sociaux",
                "entreprise": ent3,
                "domaine": "Marketing & Communication",
                "lieu": OffreStage.Ville.ABIDJAN,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=20),
                "date_limite": today + timedelta(days=55),
                "description": (
                    "Création de contenus éditoriaux, gestion du calendrier social media, suivi des campagnes "
                    "publicitaires et analyse des statistiques d'audience."
                ),
                "competences_requises": "Rédaction web, Canva/Photoshop, community management, créativité.",
            },
            {
                "titre": "Stagiaire Conducteur de Travaux BTP",
                "entreprise": ent4,
                "domaine": "Génie Civil & BTP",
                "lieu": OffreStage.Ville.BOBO_DIOULASSO,
                "duree_mois": 6,
                "date_debut": today + timedelta(days=18),
                "date_limite": today + timedelta(days=48),
                "description": (
                    "Suivi quotidien de chantiers de construction, contrôle qualité des matériaux, "
                    "coordination des sous-traitants et rédaction des rapports d'avancement."
                ),
                "competences_requises": "AutoCAD, lecture de plans, notions de métré et sécurité chantier.",
            },
            {
                "titre": "Assistant Ressources Humaines & Recrutement",
                "entreprise": ent5,
                "domaine": "Ressources Humaines",
                "lieu": OffreStage.Ville.DAKAR,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=22),
                "date_limite": today + timedelta(days=52),
                "description": (
                    "Tri des candidatures, planification des entretiens, gestion administrative des dossiers "
                    "du personnel et appui à l'organisation des formations internes."
                ),
                "competences_requises": "Sens relationnel, droit du travail, maîtrise du pack Office.",
            },
            {
                "titre": "Stage Gestion de la Chaîne Logistique (Supply Chain)",
                "entreprise": ent4,
                "domaine": "Logistique & Transport",
                "lieu": OffreStage.Ville.LOME,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=25),
                "date_limite": today + timedelta(days=60),
                "description": (
                    "Suivi des approvisionnements, gestion des stocks en entrepôt, planification des livraisons "
                    "régionales et optimisation des coûts de transport."
                ),
                "competences_requises": "Gestion des stocks, Excel, organisation et esprit analytique.",
            },
            {
                "titre": "Technicien Suivi de Projets Agricoles Durables",
                "entreprise": ent5,
                "domaine": "Agronomie & Environnement",
                "lieu": OffreStage.Ville.BOBO_DIOULASSO,
                "duree_mois": 5,
                "date_debut": today + timedelta(days=14),
                "date_limite": today + timedelta(days=45),
                "description": (
                    "Accompagnement des coopératives partenaires sur le terrain, collecte de données agronomiques, "
                    "suivi de l'irrigation solaire et rédaction de fiches techniques."
                ),
                "competences_requises": "Bases en agronomie, travail de terrain, rédaction de rapports.",
            },
            {
                "titre": "Stagiaire Juriste d'Entreprise & Contrats",
                "entreprise": ent3,
                "domaine": "Droit & Juridique",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=28),
                "date_limite": today + timedelta(days=58),
                "description": (
                    "Rédaction et relecture de contrats commerciaux, veille juridique OHADA, préparation de dossiers "
                    "réglementaires et accompagnement de la direction juridique."
                ),
                "competences_requises": "Droit des affaires OHADA, rédaction juridique, esprit de synthèse.",
            },
            {
                "titre": "Assistant Commercial & Développement B2B",
                "entreprise": ent5,
                "domaine": "Commerce & Gestion",
                "lieu": OffreStage.Ville.COTONOU,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=16),
                "date_limite": today + timedelta(days=46),
                "description": (
                    "Prospection de nouveaux clients professionnels, élaboration de devis commerciaux, "
                    "suivi du portefeuille clients et participation aux rendez-vous de négociation."
                ),
                "competences_requises": "Techniques de vente, aisance orale, CRM et autonomie.",
            },
            {
                "titre": "Stage Contrôle de Gestion & Reporting (Session précédente)",
                "entreprise": ent3,
                "domaine": "Finance & Comptabilité",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 3,
                "date_debut": today - timedelta(days=20),
                "date_limite": today - timedelta(days=5),
                "description": (
                    "Suivi budgétaire mensuel, élaboration de tableaux de bord financiers et analyse des écarts "
                    "pour la direction générale."
                ),
                "competences_requises": "Contrôle de gestion, Excel, analyse financière.",
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
