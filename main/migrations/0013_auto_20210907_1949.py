# Generated by Django 3.2 on 2021-09-07 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_rename_enviada_grupo_registrado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='disponibilidad',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='title',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
