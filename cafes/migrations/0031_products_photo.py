# Generated by Django 4.1.3 on 2023-09-01 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0030_orderprod_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='photo',
            field=models.ImageField(blank=True, upload_to='products/pic/%Y/%m/%d/'),
        ),
    ]
