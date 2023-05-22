from django import forms
from django.core.exceptions import ValidationError
from .models import Machine,Personnel,Infrastructure
from datetime import datetime
from django.forms.widgets import DateInput


class AddMachineForm(forms.Form) :

    nom = forms.CharField(required=True, label = 'Nom de la machine', widget=forms.TextInput(attrs={'class':'form-control'}))
    mach = forms.ChoiceField(choices=Machine.TYPE, label='Type de machine')
    address_ip = forms.CharField(required=True, label = 'Addresse Ip de la machine', widget=forms.TextInput(attrs={'class':'form-control'}))
    personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label='Personnel attribuée')
    creation_date = forms.DateField(widget=DateInput(attrs={'type': 'date','class':'form-control'}), label='Date de la prochaine maintenance')
    site = forms.ChoiceField(choices=Personnel.SITE, label='Site')
    dministrateur = forms.ModelChoiceField(queryset=Personnel.objects.filter(role='Administrateur'), label='Personnel attribuée')
                

   

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 12:
            raise ValidationError(('Erreur de format pour le champ nom'))
        
        return data
class AddInfrastructureForm(forms.Form) :
    nom = forms.CharField(required=True, label = "Nom de l'infrastructure")

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))
    



class AddPersonnelForm(forms.Form) :
    nom = forms.CharField(required=True, label = 'Nom du personnel')
    prenom = forms.CharField(required=True, label = 'Prenom du personnel')
    genre = forms.ChoiceField(choices=Personnel.GENRE, label='Genre')
    site = forms.ChoiceField(choices=Personnel.SITE, label='Site')
    machine = forms.ModelChoiceField(queryset=Machine.objects.all(), label='Machine attribuée')
    role = forms.ChoiceField(choices=Personnel.ROLE, label='Role')
    email = forms.EmailField(required=True, label='Email du personnel')
    telephone = forms.CharField(required=True, label = 'Numéro de téléphone')
    
       


    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))

    def clean_nom(self):
        data = self.cleaned_data["telephone"]
        if len(data) == 10:
            raise ValidationError(('Erreur de format pour le champ nom'))

        return data
    def clean_prenom(self):
        data = self.cleaned_data["prenom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))

        return data
     