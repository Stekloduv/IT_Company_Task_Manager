# Generated by Django 5.1.1 on 2024-10-07 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="manager.position",
            ),
        ),
    ]
