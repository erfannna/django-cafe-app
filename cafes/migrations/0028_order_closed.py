# Generated by Django 4.1.3 on 2023-06-01 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0027_alter_cafe_premium_exp_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]