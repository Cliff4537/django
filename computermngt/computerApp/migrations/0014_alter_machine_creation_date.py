# Generated by Django 4.1.7 on 2023-06-03 11:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0013_alter_infrastructure_machines_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="creation_date",
            field=models.DateField(
                default=datetime.datetime(2023, 6, 3, 11, 39, 30, 743847)
            ),
        ),
    ]