# Generated by Django 3.2 on 2021-09-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210902_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='num_reserva',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='reservada',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]