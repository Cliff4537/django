# Generated by Django 4.1.7 on 2023-05-15 21:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0017_remove_machine_administrateur_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="machine",
            name="aadministrateur",
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
        migrations.AlterField(
            model_name="machine",
            name="maintenanceDate",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 15, 21, 3, 36, 570800)
            ),
        ),
    ]
