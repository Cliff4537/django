from django.db import models
from django.core.validators import RegexValidator, validate_ipv4_address
from datetime import datetime

class Machine(models.Model):
        TYPE = (
                ('PC', ('Windows')),
                ('Mac', ('MacOS')),
                ('Serveur', ('Serveur')),
                ('Switch', ('Switch' )),
        )

        id = models.AutoField(
                primary_key=True,
                editable=False)
        nom= models.CharField(
            max_length =6
    )
        maintenanceDate = models.DateField(default = datetime.now())
        mach = models.CharField(max_length=32, choices=TYPE, default='PC')
        address_ip = models.GenericIPAddressField(protocol='IPv4',
         validators=[RegexValidator(
            regex=r'^(?!0\.0\.0\.0$)',
            message='The IP address "0.0.0.0" can only be used as the default value',
        ), validate_ipv4_address],
        unique=True,
        default='0.0.0.0',
    )
        

        def __str__ (self):
          return str(self.id) + " -> " + self.nom
        def get_name(self):
          return str(self.id) + " " + self.nom


class Personnel(models.Model):
        id = models.AutoField(
                primary_key=True,
                editable=False
        )
        nom = models.CharField(
            max_length=50,
        )
        prenom = models.CharField(
            max_length=50
        )
        GENRE = (
                ('Homme', ('Homme')),
                ('Femme', ('Femme')),
                ('Autre', ('Autre'))
        )
        SITE = (
                ('Tours', ('Tours')),
                ('Paris',('Paris'))
        )
        prenom = models.CharField(
                max_length=50
        )
        ROLE = (
                ('Utilisateur',('Utilisateur')),
                ('Administrateur', ('Administrateur'))
        )
        telephone=models.CharField(max_length=10, default='None')
        email = models.EmailField(blank=True, default='None')
        genre = models.CharField(max_length=32, choices=GENRE,default='Autre')
        site = models.CharField(max_length=10, choices=SITE,default='Paris')
        role = models.CharField(max_length=15, choices=ROLE,default='Utilisateur')
        machine = models.ForeignKey('Machine', null=True, blank=True, on_delete=models.SET_NULL,)

        def __str__ (self):
          return str(self.id) + " -> " + self.nom + self.prenom

        def get_name(self):
          return str(self.id) + " " + self.nom



# Create your models here.
