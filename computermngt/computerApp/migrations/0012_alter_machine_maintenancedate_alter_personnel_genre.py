# Generated by Django 4.1.7 on 2023-05-14 15:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0011_alter_machine_maintenancedate_alter_personnel_genre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="maintenanceDate",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 14, 15, 43, 18, 654156)
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="genre",
            field=models.CharField(
                choices=[("Mr", "Homme"), ("Mme", "Femme"), ("", "Autre")],
                default="Autre",
                max_length=32,
            ),
        ),
    ]
