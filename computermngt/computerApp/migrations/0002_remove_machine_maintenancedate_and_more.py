# Generated by Django 4.1.7 on 2023-06-05 17:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="machine",
            name="maintenanceDate",
        ),
        migrations.AddField(
            model_name="machine",
            name="administrateur",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to=models.Q(
                    ("role", "Administrateur"), ("site", models.F("site"))
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="administrateur_machines",
                to="computerApp.personnel",
            ),
        ),
        migrations.AddField(
            model_name="machine",
            name="creation_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="machine",
            name="maintenance_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="machine",
            name="personnel",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="machine_attitre",
                to="computerApp.personnel",
            ),
        ),
        migrations.AddField(
            model_name="machine",
            name="site",
            field=models.CharField(
                choices=[("Tours", "Tours"), ("Paris", "Paris")],
                default="Paris",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="address_ip",
            field=models.GenericIPAddressField(
                default="0.0.0.0",
                protocol="IPv4",
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(regex="^(?!0\\.0\\.0\\.0$)"),
                    django.core.validators.validate_ipv4_address,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="nom",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="genre",
            field=models.CharField(
                choices=[("Mr", "Homme"), ("Mme", "Femme")],
                default="Homme",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="machine",
            field=models.OneToOneField(
                blank=True,
                default="None",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="personnel_attitre",
                to="computerApp.machine",
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="site",
            field=models.CharField(
                choices=[("Tours", "Tours"), ("Paris", "Paris")],
                default="Paris",
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="telephone",
            field=models.CharField(
                default="None",
                max_length=10,
                validators=[django.core.validators.MaxValueValidator(10)],
            ),
        ),
        migrations.CreateModel(
            name="MiseAJourMachine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "administrateur",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to=models.Q(("role", "Administrateur")),
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mises_a_jour",
                        to="computerApp.personnel",
                    ),
                ),
                (
                    "machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mises_a_jour",
                        to="computerApp.machine",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Infrastructure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=50)),
                (
                    "site",
                    models.CharField(
                        choices=[("Tours", "Tours"), ("Paris", "Paris")],
                        default="Paris",
                        max_length=15,
                    ),
                ),
                (
                    "administrateur",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to=models.Q(
                            ("role", "Administrateur"), ("site", models.F("site"))
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="administrateur_infrastructure",
                        to="computerApp.personnel",
                    ),
                ),
                (
                    "machines",
                    models.ManyToManyField(
                        blank=True,
                        limit_choices_to=models.Q(("site", models.F("site"))),
                        related_name="infrastructures",
                        to="computerApp.machine",
                    ),
                ),
            ],
        ),
    ]
