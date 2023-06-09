# Generated by Django 4.1.7 on 2023-03-17 10:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("computerApp", "0002_personnel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="personnel",
            name="id",
        ),
        migrations.AlterField(
            model_name="personnel",
            name="N_secu",
            field=models.CharField(
                default="null",
                editable=False,
                max_length=13,
                primary_key=True,
                serialize=False,
                validators=[django.core.validators.RegexValidator("^\\d{13,13}$")],
            ),
        ),
    ]
