# Generated by Django 4.2.5 on 2025-01-01 01:00

import campaigns.models
import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_alter_campaignmodel_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignmodel',
            name='end_date',
            field=models.DateTimeField(default=campaigns.models.in_fourteen_days, validators=[django.core.validators.MinValueValidator(datetime.datetime(2025, 1, 1, 1, 0, 32, 763844, tzinfo=datetime.timezone.utc), "Date should not be less that today's date")]),
        ),
    ]