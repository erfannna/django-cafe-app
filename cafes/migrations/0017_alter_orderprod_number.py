# Generated by Django 4.1.3 on 2022-12-15 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0016_alter_orderprod_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderprod',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
