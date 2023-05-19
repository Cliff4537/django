# Generated by Django 4.1.7 on 2023-05-15 20:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0016_alter_machine_maintenancedate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="machine",
            name="administrateur",
        ),
        migrations.AddField(
            model_name="machine",
            name="aadministrateur",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to=models.Q(("role", "Administrateur")),
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
                default=datetime.datetime(2023, 5, 15, 20, 17, 43, 834747)
            ),
        ),
    ]