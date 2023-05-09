from django import forms
from django.core.exceptions import ValidationError
from .models import Machine

class AddMachineForm(forms.Form) :

    nom = forms.CharField(required=True, label = 'Nom de la machine')
    mach = forms.ChoiceField(choices=Machine.TYPE, label='Type de machine')

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 6:
            raise ValidationError(('Erreur de format pour le champ nom'))
        
        return data
    # TYPE = forms.CharField(required=True, label = 'Type de machine')

    # def clean_TYPE(self):
    #     data = self.cleaned_data["TYPE"]
    #     if len(data) != 6:
    #         raise ValidationError(('Erreur de format pour le champ nom'))
        
    #     return data



class AddPersonnelForm(forms.Form) :
    secu = forms.CharField(required=True, label = 'Numero de secu')
    nom = forms.CharField(required=True, label = 'Nom du personnel')
    
    def clean_secu(self):
        data = self.cleaned_data["secu"]
        if len(data) > 13:
            raise ValidationError(('Erreur de format pour le champ secu'))
        return data    


    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if len(data) > 50:
            raise ValidationError(('Erreur de format pour le champ nom'))

        return data    