# Generated by Django 4.1.7 on 2023-05-13 07:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0008_alter_machine_maintenancedate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="maintenanceDate",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 13, 7, 47, 2, 971654)
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="genre",
            field=models.CharField(
                choices=[("Homme", "Homme"), ("Femme", "Femme"), ("Autre", "Autre")],
                default="Autre",
                max_length=32,
            ),
        ),
    ]
