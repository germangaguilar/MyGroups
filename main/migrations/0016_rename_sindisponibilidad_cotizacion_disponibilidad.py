# Generated by Django 3.2 on 2021-09-08 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20210908_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cotizacion',
            old_name='sindisponibilidad',
            new_name='disponibilidad',
        ),
    ]
