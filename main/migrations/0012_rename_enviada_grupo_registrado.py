# Generated by Django 3.2 on 2021-09-07 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210907_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grupo',
            old_name='enviada',
            new_name='registrado',
        ),
    ]
