# Generated by Django 4.1.3 on 2023-06-03 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0028_order_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='closed',
            field=models.BooleanField(default=True),
        ),
    ]
