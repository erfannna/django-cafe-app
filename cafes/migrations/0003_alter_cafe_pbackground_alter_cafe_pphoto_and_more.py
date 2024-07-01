# Generated by Django 4.1.3 on 2022-12-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0002_menu_qr_alter_cafe_map_link_alter_cafe_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='pBackground',
            field=models.ImageField(blank=True, upload_to='profiles/<built-in function id>/'),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='pPhoto',
            field=models.ImageField(blank=True, upload_to='profiles/pic/<built-in function id>/'),
        ),
        migrations.AlterField(
            model_name='templates',
            name='htmlFile',
            field=models.FileField(blank=True, upload_to='templates/<built-in function id>/'),
        ),
    ]
