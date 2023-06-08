from django import forms
from django.core.exceptions import ValidationError
from .models import Machine,Personnel,Infrastructure
from datetime import datetime
from django.forms.widgets import DateInput
from django.forms import CheckboxSelectMultiple
import ipaddress


class AddMachineForm(forms.Form):
    nom = forms.CharField(required=True, label='(*)Nom de la machine', widget=forms.TextInput(attrs={'class':'form-control'}))
    mach = forms.ChoiceField(choices=Machine.TYPE, label='(*)Type de machine')
    address_ip = forms.CharField(required=True, label='(*)Adresse IP de la machine', widget=forms.TextInput(attrs={'class':'form-control'}))
    personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label='Personnel attribué', required=False)
    creation_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class':'form-control'}), label='Date de création de la machine')
    site = forms.ChoiceField(choices=Personnel.SITE, label='(*)Site')
    administrateur = forms.ModelChoiceField(queryset=Personnel.objects.filter(role='Administrateur'), label='Administrateur local',required=False)

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 12:
            raise ValidationError(('Erreur de format pour le champ nom'))
        return data

    def clean_address_ip(self):
        address_ip = self.cleaned_data["address_ip"]
        octets = address_ip.split(".")
    
        if len(octets) != 4:
            raise ValidationError(('Adresse IP invalide'))

        for octet in octets:
            if not octet.isdigit() or int(octet) > 255:
                raise ValidationError(('L\'adresse IP est incorrecte'))

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
                self.add_error('nom', 'Une machine de même nom et type similaire existe déjà')

        return cleaned_data
    def clean_administrateur(self):
        administrateur = self.cleaned_data.get('administrateur')
        site = self.cleaned_data.get('site')

        if administrateur and administrateur.role != 'Administrateur':
            raise forms.ValidationError("L'administrateur doit avoir le rôle 'Administrateur'.")

        if administrateur and administrateur.site != site:
            raise forms.ValidationError("L'administrateur doit appartenir au même site.")

        return administrateur

    
class AddInfrastructureForm(forms.ModelForm):
    machines = forms.ModelMultipleChoiceField(
        queryset=Machine.objects.filter(),
        widget=forms.CheckboxSelectMultiple,  # Utilisation du widget CheckboxSelectMultiple
        required=True
    )

    class Meta:
        model = Infrastructure
        fields = ['nom', 'site', 'administrateur']

    

    def clean(self):
        cleaned_data = super().clean()
        administrateur = cleaned_data.get('administrateur')
        site = cleaned_data.get('site')

        if administrateur and site:
            infrastructures_count = Infrastructure.objects.filter(
                administrateur=administrateur,
                site=site
            ).exclude(pk=self.instance.pk).count()

            if infrastructures_count > 0:
                self.add_error('administrateur', "Cet administrateur appartient déjà à une autre infrastructure.")

        return cleaned_data

class AddPersonnelForm(forms.Form):
    nom = forms.CharField(required=True, label='Nom du personnel')
    prenom = forms.CharField(required=True, label='Prenom du personnel')
    genre = forms.ChoiceField(choices=Personnel.GENRE, label='Genre')
    site = forms.ChoiceField(choices=Personnel.SITE, label='Site')
    machine = forms.ModelChoiceField(queryset=Machine.objects.all(), required=False, label='Machine attribuée')
    role = forms.ChoiceField(choices=Personnel.ROLE, label='Role')
    email = forms.EmailField(required=True, label='Email du personnel')
    telephone = forms.CharField(required=False, label='Numéro de téléphone')

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))
        return data

    def clean_telephone(self):
        data = self.cleaned_data["telephone"]
        if len(data) != 10:
            raise ValidationError(('Erreur de format pour le champ téléphone (10 caractères) '))
        return data

    def clean_prenom(self):
        data = self.cleaned_data["prenom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ prénom'))
        if len(data) <= 0:
            raise ValidationError(('Le champ prénom est obligatoire'))
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
    
    def clean_machine(self):
        machine = self.cleaned_data.get("machine")
        if machine is None:
            return None  # Retourne None si le champ est vide
        personnel_with_machine = Personnel.objects.filter(machine=machine).exists()
        if personnel_with_machine:
            raise ValidationError('Cette machine est déjà attribuée.')
        return machine









