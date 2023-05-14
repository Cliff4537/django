from django import forms
from django.core.exceptions import ValidationError
from .models import Machine,Personnel

class AddMachineForm(forms.Form) :

    nom = forms.CharField(required=True, label = 'Nom de la machine')
    mach = forms.ChoiceField(choices=Machine.TYPE, label='Type de machine')
    address_ip = forms.CharField(required=True, label = 'Addresse Ip de la machine')
    personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label='Personnel attribuée')
    
    

    # Vérifie si le personnel est déjà affecté à une machine
    # def clean_personnel(self):
    #     personnel = self.cleaned_data.get('personnel')
    #     if personnel:
            
    #         if personnel.machine:
    #             raise ValidationError('Cet utilisateur est déjà affecté à une machine')
    #     return personnel

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 12:
            raise ValidationError(('Erreur de format pour le champ nom'))
        
        return data

    #personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label='Personne attribuée')
    # TYPE = forms.CharField(required=True, label = 'Type de machine')

    # def clean_TYPE(self):
    #     data = self.cleaned_data["TYPE"]
    #     if len(data) != 6:
    #         raise ValidationError(('Erreur de format pour le champ nom'))
        
    #     return data



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
     