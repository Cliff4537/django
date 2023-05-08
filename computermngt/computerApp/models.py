from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime

class Machine(models.Model):
        TYPE = (
                ('PC', ('PC - Run windows')),
                ('Mac', ('MAC - Run MacOS')),
                ('Serveur', ('Serveur - Simple Server to deploy virtual machines')),
                ('Switch', ('Switch - Tom maintains and connect servers ' )),
        )

        id = models.AutoField(
                primary_key=True,
                editable=False)
        nom= models.CharField(
            max_length= 6
    )
        maintenanceDate = models.DateField(default = datetime.now())
        mach = models.CharField(max_length=32, choices=TYPE, default='PC')
    # MAC_ADDRESS= models.CharField(
    #         max_length= 12,
    #         null=False
    

        def __str__ (self):
          return str(self.id) + " -> " + self.nom
        def get_name(self):
          return str(self.id) + " " + self.nom


class Personnel(models.Model):
        secu = models.CharField(
            max_length=13,
            validators=[RegexValidator(r'^\d{13,13}$')],
            primary_key=True)
        
        nom = models.CharField(
            max_length=50
        )
        prenom = models.CharField(
            max_length=50
        )

def __str__ (self):
        return self.N_secu + " -> " + self.nom + self.prenom

def get_id(self):
        return str(self.id) + " " + self.N_secu

def get_last_name(self):
        return str(self.id) + " " + self.prenom

def get_name(self):
        return str(self.id) + " " + self.nom



# Create your models here.
