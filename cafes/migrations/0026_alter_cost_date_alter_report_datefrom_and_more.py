# Generated by Django 4.1.3 on 2023-01-28 12:06

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0025_report_datefrom_report_dateto_alter_cost_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='report',
            name='dateFrom',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='report',
            name='dateTo',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
