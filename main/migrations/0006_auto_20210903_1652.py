# Generated by Django 3.2 on 2021-09-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210903_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='enviada',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='reservada',
            field=models.BooleanField(default=False),
        ),
    ]
