# StageAcad — Plateforme de Gestion des Stages Académiques (Django)

Application web full-stack réalisée avec **Django** et **Tailwind CSS** pour gérer tout le cycle de vie des stages académiques :

- **Offres de stage** : publication, modification, suppression, recherche et filtrage par domaine et lieu.
- **Candidatures** : dépôt de candidature (lettre de motivation + CV) par les étudiants, acceptation ou refus par l'entreprise (l'acceptation crée automatiquement le stage).
- **Affectation des encadreurs** : l'administrateur affecte un encadreur académique à chaque stage validé.
- **Suivi des stages** : dépôt de rapports d'avancement (avec pourcentage et pièce jointe) par l'étudiant, révision/validation commentée par l'encadreur et évaluation finale (`/20`).

## Lancement rapide

```powershell
# 1. Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# 2. Appliquer les migrations (déjà fait)
python manage.py migrate

# 3. Charger les données de démonstration (déjà fait)
python manage.py seed_data

# 4. Lancer le serveur de développement
python manage.py runserver
```

Ouvrez ensuite `http://127.0.0.1:8000/`.

## Comptes de démonstration

| Rôle | Nom d'utilisateur | Mot de passe |
|---|---|---|
| Administrateur | `admin` | `admin123` |
| Entreprise | `techvision` / `datanexus` | `demo1234` |
| Encadreur académique | `prof_dupont` / `prof_kone` | `demo1234` |
| Étudiant | `etudiant1` / `etudiant2` / `etudiant3` | `demo1234` |
