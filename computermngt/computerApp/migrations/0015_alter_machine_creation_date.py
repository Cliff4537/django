# Generated by Django 4.1.7 on 2023-06-03 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0014_alter_machine_creation_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(2023, 6, 3, 15, 29, 7, 952688)
            ),
        ),
    ]
