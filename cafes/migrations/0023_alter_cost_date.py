# Generated by Django 4.1.3 on 2023-01-18 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0022_alter_cost_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 18, 16, 36, 43, 709321)),
        ),
    ]
