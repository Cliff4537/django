# Generated by Django 4.1.7 on 2023-05-29 08:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0002_remove_machine_maintenancedate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 29, 8, 23, 47, 405981)
            ),
        ),
    ]