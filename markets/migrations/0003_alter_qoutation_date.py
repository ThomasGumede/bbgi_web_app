# Generated by Django 4.2.5 on 2025-01-01 00:13

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0002_alter_qoutation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qoutation',
            name='date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.datetime(2025, 1, 1, 0, 13, 29, 183807, tzinfo=datetime.timezone.utc), "Date should not be less that today's date")]),
        ),
    ]
