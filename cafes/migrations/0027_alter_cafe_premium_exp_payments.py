# Generated by Django 4.1.3 on 2023-05-04 13:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cafes', '0026_alter_cost_date_alter_report_datefrom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='premium_exp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='panel_charge', max_length=20)),
                ('status', models.CharField(default='success', max_length=15)),
                ('price', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafe_payments', to='cafes.cafe')),
            ],
        ),
    ]
