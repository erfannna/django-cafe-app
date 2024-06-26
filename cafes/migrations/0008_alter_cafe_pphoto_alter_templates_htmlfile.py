# Generated by Django 4.1.3 on 2022-12-08 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0007_alter_templates_htmlfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='pPhoto',
            field=models.ImageField(blank=True, upload_to='profiles/pic/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='templates',
            name='htmlFile',
            field=models.FileField(blank=True, upload_to='templates/%id'),
        ),
    ]
