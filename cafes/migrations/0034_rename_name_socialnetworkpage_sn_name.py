# Generated by Django 4.1.3 on 2023-09-09 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0033_alter_cafe_phonenum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialnetworkpage',
            old_name='name',
            new_name='sn_name',
        ),
    ]
