# Generated by Django 4.1.3 on 2022-12-08 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0006_alter_cafe_pbackground_alter_cafe_pphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates',
            name='htmlFile',
            field=models.FileField(blank=True, upload_to='templates/<built-in function id>/'),
        ),
    ]
