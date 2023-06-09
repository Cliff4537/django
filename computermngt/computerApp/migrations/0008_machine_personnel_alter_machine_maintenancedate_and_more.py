# Generated by Django 4.1.7 on 2023-05-14 15:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0007_alter_machine_maintenancedate_alter_personnel_genre"),
    ]

    operations = [
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
        migrations.AlterField(
            model_name="machine",
            name="maintenanceDate",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 14, 15, 37, 13, 654758)
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="genre",
            field=models.CharField(
                choices=[("Homme", "Monsieur"), ("Femme", "Madame"), ("Autre", "")],
                default="Autre",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="machine",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="personnel_attitre",
                to="computerApp.machine",
            ),
        ),
    ]
