# Generated by Django 4.1.7 on 2023-05-29 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0007_alter_machine_creation_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 29, 15, 30, 20, 403769)
            ),
        ),
    ]
