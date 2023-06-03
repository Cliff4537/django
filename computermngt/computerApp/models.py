from django.db import models
from django.core.validators import RegexValidator, validate_ipv4_address, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta
from django.db.models import Q

class Machine(models.Model):
    TYPE = (
        ('PC', 'Windows'),
        ('Mac', 'MacOS'),
        ('Serveur', 'Serveur'),
        ('Switch', 'Switch'),
    )

    id = models.AutoField(primary_key=True, editable=False)
    nom = models.CharField(max_length=30)
    creation_date = models.DateField(default=datetime.now())
    mach = models.CharField(max_length=32, choices=TYPE, default='PC')
    address_ip = models.GenericIPAddressField(
        protocol='IPv4',
        validators=[
            RegexValidator(
                regex=r'^(?!0\.0\.0\.0$)'  
            ),
            validate_ipv4_address
        ],
        unique=True,
        default='0.0.0.0'
    )
    SITE = (
        ('Tours', 'Tours'),
        ('Paris', 'Paris')
    )
    site = models.CharField(max_length=10, choices=SITE, default='Paris')
    personnel = models.OneToOneField('Personnel', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='machine_attitre')
    administrateur = models.ForeignKey(
        'Personnel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='administrateur_machines',
        limit_choices_to=Q(role='Administrateur') & Q(site=models.F('site'))
    )

    def __str__(self):
        return f"{self.site} - {self.mach} - {self.nom}"

    def get_name(self):
        return f"{self.id} {self.nom}"
    
    


class Personnel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    GENRE = (
        ('Mr', 'Homme'),
        ('Mme', 'Femme'),

    )
    SITE = (
        ('Tours', 'Tours'),
        ('Paris', 'Paris')
    )
    ROLE = (
        ('Utilisateur', 'Utilisateur'),
        ('Administrateur', 'Administrateur')
    )
    telephone = models.CharField(
        max_length=10,
        validators=[MaxValueValidator(10)],
        default='None'
    )
    email = models.EmailField(blank=True, default='None')
    genre = models.CharField(max_length=32, choices=GENRE, default='Homme')
    site = models.CharField(max_length=15, choices=SITE, default='Paris')
    role = models.CharField(max_length=15, choices=ROLE, default='Utilisateur')
    machine = models.OneToOneField('Machine', on_delete=models.SET_NULL, null=True, blank=True,default='None',
                                   related_name='personnel_attitre')

    def __str__(self):
        return f"{self.id} - {self.genre}.{self.nom} {self.prenom}"

    def get_name(self):
        return f"{self.id} {self.nom}"



class Infrastructure(models.Model):
    nom = models.CharField(max_length=50)
    SITE = (
        ('Tours', 'Tours'),
        ('Paris', 'Paris')
    )
    site = models.CharField(max_length=15, choices=SITE, default='Paris')

    administrateur = models.ForeignKey(
        'Personnel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='administrateur_infrastructure',
        limit_choices_to=Q(role='Administrateur') & Q(site=models.F('site'))
    )
    machines = models.ManyToManyField(
        'Machine',
        related_name='infrastructures',
        blank=True,
        limit_choices_to=Q(site=models.F('site'))
    )

    def __str__(self):
        return self.nom

    def clean(self):
        super().clean()
        if self.administrateur and self.administrateur.administrateur_infrastructure.exists():
            raise ValidationError("Un administrateur ne peut être associé qu'à une seule infrastructure.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
