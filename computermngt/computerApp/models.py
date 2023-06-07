from django.db import models
from django.core.validators import RegexValidator, validate_ipv4_address, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User

class MiseAJourMachine(models.Model):
    machine = models.ForeignKey(
        'Machine',
        on_delete=models.CASCADE,
        related_name='mises_a_jour'
    )
    administrateur = models.ForeignKey(
        'Personnel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mises_a_jour',
        limit_choices_to=Q(role='Administrateur')
    )
    date = models.DateTimeField(auto_now_add=True)

class Machine(models.Model):
    TYPE = (
        ('PC', 'Windows'),
        ('Mac', 'MacOS'),
        ('Serveur', 'Serveur'),
        ('Switch', 'Switch'),
    )
   
#     ETAT_CHOICES = (
#     ('1', 'Vert'),
#     ('2', 'Jaune'),
#     ('3', 'Rouge'),
#     ('4', 'Violet'),
# )


    id = models.AutoField(primary_key=True, editable=False)
    nom = models.CharField(max_length=30)
    # etat = models.IntegerField(choices=ETAT_CHOICES, default='1')
    creation_date = models.DateTimeField(auto_now_add=True)
    maintenance_date = models.DateTimeField(null=True, blank=True)
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
    
    def save(self, *args, **kwargs):
        if not self.maintenance_date:
            self.maintenance_date = self.calculate_maintenance_date()
        super().save(*args, **kwargs)


    def calculate_maintenance_date(self):
        if self.mach == 'PC':
            maintenance_delta = timedelta(days=7)
        elif self.mach == 'Mac':
            maintenance_delta = timedelta(days=7)
        elif self.mach == 'Serveur':
            maintenance_delta = timedelta(days=14)
        elif self.mach == 'Switch':
            maintenance_delta = timedelta(days=28)
        else:
            maintenance_delta = timedelta(days=0)
            

        return self.creation_date + maintenance_delta

class MachineUpdate(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Machine: {self.machine.nom} | Admin: {self.admin.username} | Update Date: {self.update_date}"

# Tentative de changement de fond d'écran en fonction du nomdre de jours restant
#     def update_etat(self):
#      if self.maintenance_date is not None:
#         remaining_days = (self.maintenance_date - timezone.localdate()).days
#         if remaining_days > 3:
#             self.etat = 1
#         elif remaining_days >= 0:
#             self.etat = 2
#         elif remaining_days >= -1:
#             self.etat = 3
#         else:
#             self.etat = 4
#      else:
#         self.etat = 4

# def get_etat_class(self):
#     if self.etat == 1:
#         return 'bg-success'
#     elif self.etat == 2:
#         return 'bg-warning'
#     elif self.etat == 3:
#         return 'bg-danger'
#     elif self.etat == 4:
#         return 'bg-purple'
#     else:
#         return ''


    
    


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
        return f"{self.genre}.{self.nom} {self.prenom}"

    def get_name(self):
        return f"{self.nom}"



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
        
