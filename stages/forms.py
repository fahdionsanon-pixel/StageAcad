from django import forms
from accounts.models import User
from .models import Candidature, OffreStage, RapportSuivi, Stage

INPUT_CLASS = (
    "w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm text-slate-900 "
    "shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
)


class OffreStageForm(forms.ModelForm):
    class Meta:
        model = OffreStage
        fields = (
            "titre",
            "domaine",
            "lieu",
            "duree_mois",
            "date_debut",
            "date_limite",
            "description",
            "competences_requises",
            "est_active",
        )
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "date_limite": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "description": forms.Textarea(attrs={"rows": 5, "class": INPUT_CLASS}),
            "competences_requises": forms.Textarea(attrs={"rows": 3, "class": INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "est_active":
                field.widget.attrs["class"] = "h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            elif "class" not in field.widget.attrs:
                field.widget.attrs["class"] = INPUT_CLASS


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ("lettre_motivation", "cv")
        widgets = {
            "lettre_motivation": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": INPUT_CLASS,
                    "placeholder": "Présentez votre parcours, votre motivation et vos disponibilités...",
                }
            ),
            "cv": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 "
                    "file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-blue-700 "
                    "hover:file:bg-blue-100"
                }
            ),
        }


class AffectationEncadreurForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ("encadreur", "statut")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["encadreur"].queryset = User.objects.filter(role=User.Role.ENCADREUR, is_active=True).order_by(
            "last_name", "first_name"
        )
        self.fields["encadreur"].empty_label = "— Sélectionner un encadreur —"
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


class EvaluationStageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ("statut", "note_finale", "appreciation_finale")
        widgets = {
            "appreciation_finale": forms.Textarea(attrs={"rows": 4, "class": INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = INPUT_CLASS


class RapportSuiviForm(forms.ModelForm):
    class Meta:
        model = RapportSuivi
        fields = ("titre", "avancement_pourcent", "contenu", "document")
        widgets = {
            "contenu": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": INPUT_CLASS,
                    "placeholder": "Décrivez les tâches réalisées, difficultés rencontrées et prochaines étapes...",
                }
            ),
            "document": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 "
                    "file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-blue-700 "
                    "hover:file:bg-blue-100"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = INPUT_CLASS


class RevisionRapportForm(forms.ModelForm):
    class Meta:
        model = RapportSuivi
        fields = ("statut", "commentaire_encadreur")
        widgets = {
            "commentaire_encadreur": forms.Textarea(
                attrs={"rows": 3, "class": INPUT_CLASS, "placeholder": "Vos remarques et recommandations..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["statut"].widget.attrs["class"] = INPUT_CLASS
