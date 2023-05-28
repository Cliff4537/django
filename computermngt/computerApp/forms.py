from django import forms
from django.core.exceptions import ValidationError
from .models import Machine,Personnel,Infrastructure
from datetime import datetime
from django.forms.widgets import DateInput


class AddMachineForm(forms.Form):
    nom = forms.CharField(required=True, label='Nom de la machine', widget=forms.TextInput(attrs={'class':'form-control'}))
    mach = forms.ChoiceField(choices=Machine.TYPE, label='Type de machine')
    address_ip = forms.CharField(required=True, label='Adresse IP de la machine', widget=forms.TextInput(attrs={'class':'form-control'}))
    personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label='Personnel attribué', required=False)
    creation_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class':'form-control'}), label='Date de la prochaine maintenance')
    site = forms.ChoiceField(choices=Personnel.SITE, label='Site')
    administrateur = forms.ModelChoiceField(queryset=Personnel.objects.filter(role='Administrateur'), label='Administrateur local',required=False)

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 12:
            raise ValidationError(('Erreur de format pour le champ nom'))
        return data

    def clean_address_ip(self):
        address_ip = self.cleaned_data["address_ip"]
        if address_ip != '0.0.0.0' and Machine.objects.filter(address_ip=address_ip).exists():
            raise ValidationError(('Cette adresse IP existe déjà'))
        return address_ip

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        mach = cleaned_data.get('mach')

        if nom and mach:
            existing_machine = Machine.objects.filter(nom=nom, mach=mach).exists()
            if existing_machine:
                self.add_error('nom', 'Une machine du même nom et type existe déjà')

        return cleaned_data

    
class AddInfrastructureForm(forms.Form) :
    nom = forms.CharField(required=True, label = "Nom de l'infrastructure")

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))
    



class AddPersonnelForm(forms.Form):
    nom = forms.CharField(required=True, label='Nom du personnel')
    prenom = forms.CharField(required=True, label='Prenom du personnel')
    genre = forms.ChoiceField(choices=Personnel.GENRE, label='Genre')
    site = forms.ChoiceField(choices=Personnel.SITE, label='Site')
    machine = forms.ModelChoiceField(queryset=Machine.objects.all(), required=False, label='Machine attribuée')
    role = forms.ChoiceField(choices=Personnel.ROLE, label='Role')
    email = forms.EmailField(required=True, label='Email du personnel')
    telephone = forms.CharField(required=True, label='Numéro de téléphone')

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))
        return data

    def clean_telephone(self):
        data = self.cleaned_data["telephone"]
        if len(data) != 10:
            raise ValidationError(('Erreur de format pour le champ téléphone'))
        return data

    def clean_prenom(self):
        data = self.cleaned_data["prenom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ prénom'))
        return data

    def clean_machine(self):
        machine = self.cleaned_data.get("machine")
        if machine is None:
            return None  # Retourne None si le champ est vide
        return machine

    def clean_email(self):
        email = self.cleaned_data["email"]
        existing_personnel = Personnel.objects.filter(email=email).exists()
        if existing_personnel:
            raise ValidationError('Cette adresse e-mail existe déjà.')
        return email