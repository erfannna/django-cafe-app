# Generated by Django 4.1.3 on 2022-12-14 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0010_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]