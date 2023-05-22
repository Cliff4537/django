from django.db import models
from django.core.validators import RegexValidator, validate_ipv4_address
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
                regex=r'^(?!0\.0\.0\.0$)',
                message='The IP address "0.0.0.0" can only be used as the default value',
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
        return f"{self.id} - {self.mach} - {self.nom}"

    def get_name(self):
        return f"{self.id} {self.nom}"
    def calculate_maintenance_date(self):
        if self.mach == 'PC' or self.mach == 'Mac':
            maintenance_duration = timedelta(days=7)
        elif self.mach == 'Serveur':
            maintenance_duration = timedelta(days=14)
        elif self.mach == 'Switch':
            maintenance_duration = timedelta(days=30)
        else:
            maintenance_duration = timedelta(days=0)
        
        return self.creation_date + maintenance_duration


class Personnel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    GENRE = (
        ('Mr', 'Homme'),
        ('Mme', 'Femme'),
        ('', 'Autre')
    )
    SITE = (
        ('Tours', 'Tours'),
        ('Paris', 'Paris')
    )
    ROLE = (
        ('Utilisateur', 'Utilisateur'),
        ('Administrateur', 'Administrateur')
    )
    telephone = models.CharField(max_length=10, default='None')
    email = models.EmailField(blank=True, default='None')
    genre = models.CharField(max_length=32, choices=GENRE, default='Autre')
    site = models.CharField(max_length=15, choices=SITE, default='Paris')
    role = models.CharField(max_length=15, choices=ROLE, default='Utilisateur')
    machine = models.OneToOneField('Machine', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='personnel_attitre')

    def __str__(self):
        return f"{self.id} - {self.genre}.{self.nom} {self.prenom}"

    def get_name(self):
        return f"{self.id} {self.nom}"


class Infrastructure(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    SITE = (
        ('Tours', 'Tours'),
        ('Paris', 'Paris')
    )

    administrateur = models.ForeignKey(
        'Personnel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='administrateur_infrastructure',
        limit_choices_to=Q(role='Administrateur') & Q(site=models.F('site'))
    )
    machines = models.ManyToManyField('Machine', related_name='infrastructures', blank=True)
    site = models.CharField(max_length=15, choices=SITE, default='Paris')

    def __str__(self):
        return f"{self.nom}"

    def get_name(self):
        return f"{self.nom}"

    def clean(self):
        if self.administrateur and Infrastructure.objects.filter(administrateur__site=self.site).exists():
            raise ValidationError("L'Administrateur est déjà responsable d'un site")

        if self.machines.filter(site=self.site).exists():
            raise ValidationError("Une machine ne peut être associée qu'à un seul site.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
