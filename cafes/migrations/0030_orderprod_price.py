# Generated by Django 4.1.3 on 2023-06-03 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0029_alter_order_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderprod',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
