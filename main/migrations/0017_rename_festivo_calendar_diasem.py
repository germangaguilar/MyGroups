# Generated by Django 3.2 on 2021-10-01 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_rename_sindisponibilidad_cotizacion_disponibilidad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendar',
            old_name='festivo',
            new_name='diasem',
        ),
    ]
