# Generated by Django 4.1.3 on 2022-12-15 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0013_alter_order_prods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='prods',
            field=models.ManyToManyField(blank=True, related_name='order_products', to='cafes.orderprod'),
        ),
    ]