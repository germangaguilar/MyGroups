# Generated by Django 3.2 on 2021-08-31 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='precioplaza',
        ),
        migrations.AddField(
            model_name='calendar',
            name='precio3stars',
            field=models.FloatField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='calendar',
            name='FyGprice',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='NHprice',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
