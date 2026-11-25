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

        etu4, _ = User.objects.get_or_create(
            username="etudiant4",
            defaults={
                "first_name": "Salimata",
                "last_name": "Sawadogo",
                "email": "salimatasawadogo@gmail.com",
                "role": User.Role.ETUDIANT,
                "filiere": "Finance & Comptabilité",
                "niveau": "Master 1",
            },
        )
        etu4.set_password("demo1234")
        etu4.save()

        etu5, _ = User.objects.get_or_create(
            username="etudiant5",
            defaults={
                "first_name": "Moussa",
                "last_name": "Diallo",
                "email": "moussadiallo@gmail.com",
                "role": User.Role.ETUDIANT,
                "filiere": "Génie Civil",
                "niveau": "Licence 3",
            },
        )
        etu5.set_password("demo1234")
        etu5.save()

        etu6, _ = User.objects.get_or_create(
            username="etudiant6",
            defaults={
                "first_name": "Koffi",
                "last_name": "Mensah",
                "email": "koffimensah@gmail.com",
                "role": User.Role.ETUDIANT,
                "filiere": "Marketing & Gestion",
                "niveau": "Master 2",
            },
        )
        etu6.set_password("demo1234")
        etu6.save()

        offres_data = [
            {
                "titre": "Stage de Développement Web",
                "entreprise": ent1,
                "domaine": "Développement Web",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=20),
                "date_limite": today + timedelta(days=45),
                "description": (
                    "Vous intégrerez l'équipe produit pour concevoir et développer de nouvelles fonctionnalités "
                    "sur notre plateforme web en Django et Python."
                ),
                "competences_requises": "Python, Django, HTML/CSS, Git, bases de données relationnelles.",
            },
            {
                "titre": "Stage d'Analyse de Données",
                "entreprise": ent2,
                "domaine": "Data & IA",
                "lieu": OffreStage.Ville.BOBO_DIOULASSO,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=30),
                "date_limite": today + timedelta(days=60),
                "description": (
                    "Analyse des indicateurs de performance clients, création de tableaux de bord automatisés "
                    "et nettoyage de données."
                ),
                "competences_requises": "Python, Pandas, SQL, Excel ou Power BI.",
            },
            {
                "titre": "Stage en Administration Systèmes et Réseaux",
                "entreprise": ent1,
                "domaine": "Cloud & DevOps",
                "lieu": OffreStage.Ville.ABIDJAN,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=15),
                "date_limite": today + timedelta(days=40),
                "description": (
                    "Maintenance des serveurs Linux, gestion des sauvegardes, déploiement d'applications "
                    "et suivi du réseau interne."
                ),
                "competences_requises": "Linux, réseaux, Docker, sécurité de base.",
            },
            {
                "titre": "Stage en Intelligence Artificielle",
                "entreprise": ent2,
                "domaine": "Data & IA",
                "lieu": OffreStage.Ville.DAKAR,
                "duree_mois": 6,
                "date_debut": today + timedelta(days=25),
                "date_limite": today + timedelta(days=50),
                "description": (
                    "Préparation de jeux de données et création de modèles prédictifs pour l'analyse de tendances."
                ),
                "competences_requises": "Python, statistiques, apprentissage automatique.",
            },
            {
                "titre": "Stage de Comptabilité et Audit",
                "entreprise": ent3,
                "domaine": "Finance & Comptabilité",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=15),
                "date_limite": today + timedelta(days=45),
                "description": (
                    "Participation à la tenue comptable, rapprochements bancaires, préparation des déclarations "
                    "fiscales et appui aux missions d'audit interne."
                ),
                "competences_requises": "Comptabilité SYSCOHADA, Excel, rigueur et confidentialité.",
            },
            {
                "titre": "Stage de Communication",
                "entreprise": ent3,
                "domaine": "Marketing & Communication",
                "lieu": OffreStage.Ville.ABIDJAN,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=20),
                "date_limite": today + timedelta(days=55),
                "description": (
                    "Création de contenus éditoriaux, gestion des réseaux sociaux et suivi des campagnes "
                    "de communication."
                ),
                "competences_requises": "Rédaction web, Canva, gestion des réseaux sociaux.",
            },
            {
                "titre": "Stage de Conducteur de Travaux BTP",
                "entreprise": ent4,
                "domaine": "Génie Civil & BTP",
                "lieu": OffreStage.Ville.BOBO_DIOULASSO,
                "duree_mois": 6,
                "date_debut": today + timedelta(days=18),
                "date_limite": today + timedelta(days=48),
                "description": (
                    "Suivi quotidien de chantiers de construction, contrôle qualité des matériaux "
                    "et rédaction des rapports d'avancement."
                ),
                "competences_requises": "AutoCAD, lecture de plans, notions de métré et sécurité chantier.",
            },
            {
                "titre": "Stage en Ressources Humaines",
                "entreprise": ent5,
                "domaine": "Ressources Humaines",
                "lieu": OffreStage.Ville.DAKAR,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=22),
                "date_limite": today + timedelta(days=52),
                "description": (
                    "Tri des candidatures, planification des entretiens et gestion administrative des dossiers "
                    "du personnel."
                ),
                "competences_requises": "Sens relationnel, droit du travail, maîtrise du pack Office.",
            },
            {
                "titre": "Stage de Gestion Logistique",
                "entreprise": ent4,
                "domaine": "Logistique & Transport",
                "lieu": OffreStage.Ville.LOME,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=25),
                "date_limite": today + timedelta(days=60),
                "description": (
                    "Suivi des approvisionnements, gestion des stocks en entrepôt et planification des livraisons "
                    "régionales."
                ),
                "competences_requises": "Gestion des stocks, Excel, organisation.",
            },
            {
                "titre": "Stage d'Agronomie",
                "entreprise": ent5,
                "domaine": "Agronomie & Environnement",
                "lieu": OffreStage.Ville.BOBO_DIOULASSO,
                "duree_mois": 5,
                "date_debut": today + timedelta(days=14),
                "date_limite": today + timedelta(days=45),
                "description": (
                    "Accompagnement des coopératives partenaires sur le terrain, collecte de données agronomiques "
                    "et rédaction de fiches techniques."
                ),
                "competences_requises": "Bases en agronomie, travail de terrain, rédaction de rapports.",
            },
            {
                "titre": "Stage d'Assistant Juridique",
                "entreprise": ent3,
                "domaine": "Droit & Juridique",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 3,
                "date_debut": today + timedelta(days=28),
                "date_limite": today + timedelta(days=58),
                "description": (
                    "Rédaction et relecture de contrats commerciaux, veille juridique OHADA et préparation de dossiers."
                ),
                "competences_requises": "Droit des affaires OHADA, rédaction juridique, esprit de synthèse.",
            },
            {
                "titre": "Stage d'Assistant Commercial",
                "entreprise": ent5,
                "domaine": "Commerce & Gestion",
                "lieu": OffreStage.Ville.COTONOU,
                "duree_mois": 4,
                "date_debut": today + timedelta(days=16),
                "date_limite": today + timedelta(days=46),
                "description": (
                    "Prospection de nouveaux clients professionnels, élaboration de devis commerciaux "
                    "et suivi du portefeuille clients."
                ),
                "competences_requises": "Techniques de vente, aisance orale, autonomie.",
            },
            {
                "titre": "Stage de Contrôle de Gestion",
                "entreprise": ent3,
                "domaine": "Finance & Comptabilité",
                "lieu": OffreStage.Ville.OUAGADOUGOU,
                "duree_mois": 3,
                "date_debut": today - timedelta(days=20),
                "date_limite": today - timedelta(days=5),
                "description": (
                    "Suivi budgétaire mensuel, élaboration de tableaux de bord financiers et analyse des écarts."
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

        # Candidatures supplémentaires réalistes par des étudiants différents (sans stage actif)
        extra_cands = [
            # etudiant4 (Salimata Sawadogo - Finance) : 1 en attente en Finance + 1 refusée en DevOps
            (
                offres[4],
                etu4,
                "EN_ATTENTE",
                "Étudiante en Master 1 Finance & Comptabilité, je maîtrise le SYSCOHADA et Excel pour accompagner vos missions d'audit.",
                "",
            ),
            (
                offres[2],
                etu4,
                "REFUSEE",
                "Je souhaite découvrir l'administration de serveurs et le DevOps au sein de votre entreprise.",
                "Votre profil Finance est excellent, mais ce poste exige des bases techniques en Linux et Docker.",
            ),
            # etudiant5 (Moussa Diallo - Génie Civil) : 1 en attente en BTP + 1 refusée en Droit
            (
                offres[6],
                etu5,
                "EN_ATTENTE",
                "Étudiant en Licence 3 Génie Civil, je maîtrise AutoCAD et souhaite participer au suivi de vos chantiers à Bobo-Dioulasso.",
                "",
            ),
            (
                offres[10],
                etu5,
                "REFUSEE",
                "Je candidate au poste de stagiaire juriste pour découvrir les contrats de construction.",
                "Nous recherchons un étudiant inscrit en filière Droit des affaires OHADA pour ce stage.",
            ),
            # etudiant6 (Koffi Mensah - Marketing & Gestion) : 1 en attente en Marketing + 1 en attente Commerce + 1 refusée en Agronomie
            (
                offres[5],
                etu6,
                "EN_ATTENTE",
                "En Master 2 Marketing, je gère déjà des campagnes digitales et souhaite rejoindre votre équipe à Abidjan.",
                "",
            ),
            (
                offres[11],
                etu6,
                "EN_ATTENTE",
                "Passionné par le développement commercial B2B, je suis disponible pour 4 mois à Cotonou.",
                "",
            ),
            (
                offres[9],
                etu6,
                "REFUSEE",
                "Je souhaite accompagner vos coopératives agricoles dans le suivi de projets à Bobo-Dioulasso.",
                "Ce stage technique nécessite une formation en agronomie. Merci pour votre intérêt.",
            ),
        ]

        for offre_obj, etu_obj, statut_cible, lettre, motif in extra_cands:
            cand, created = Candidature.objects.get_or_create(
                offre=offre_obj,
                etudiant=etu_obj,
                defaults={"lettre_motivation": lettre},
            )
            if created and statut_cible == "REFUSEE":
                cand.refuser(commentaire=motif)

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès !"))
        self.stdout.write("Comptes de test :")
        self.stdout.write("  - Admin      : admin / admin123")
        self.stdout.write("  - Entreprise : techvision / demo1234  (ou datanexus / demo1234)")
        self.stdout.write("  - Encadreur  : prof_dupont / demo1234 (ou prof_kone / demo1234)")
        self.stdout.write("  - Étudiant   : etudiant1 / demo1234   (ou etudiant2, etudiant3 / demo1234)")
