# Generated by Django 3.2 on 2021-09-07 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210904_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='correo',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
