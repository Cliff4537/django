# Generated by Django 4.1.7 on 2023-05-04 09:37

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0015_alter_machine_maintenancedate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="machine",
            name="maintenanceDate",
            field=models.DateField(
                default=datetime.datetime(2023, 5, 4, 9, 37, 17, 296690)
            ),
        ),
        migrations.AlterField(
            model_name="personnel",
            name="secu",
            field=models.CharField(
                max_length=13,
                primary_key=True,
                serialize=False,
                validators=[django.core.validators.RegexValidator("^\\d{13,13}$")],
            ),
        ),
    ]
