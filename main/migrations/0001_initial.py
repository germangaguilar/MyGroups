# Generated by Django 3.2 on 2021-08-31 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('price', models.IntegerField(blank=True)),
                ('FyGprice', models.IntegerField(blank=True)),
                ('NHprice', models.IntegerField(blank=True)),
                ('rooms', models.IntegerField(blank=True)),
                ('updated', models.DateTimeField()),
                ('precioplaza', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('entrada', models.DateField()),
                ('salida', models.DateField()),
                ('pax', models.IntegerField(blank=True, default=0)),
                ('dobles', models.IntegerField(blank=True, default=0)),
                ('triples', models.IntegerField(blank=True, default=0)),
                ('DUIs', models.IntegerField(blank=True, default=0)),
                ('singles', models.IntegerField(blank=True, default=0)),
                ('comentarios', models.TextField(blank=True, default='', help_text='Comentarios adicionales', max_length=1000)),
                ('regimen', models.CharField(blank=True, choices=[('NE', 'No especificado'), ('SA', 'Solo alojamiento'), ('MP', 'Media pensión'), ('AD', 'Alojamiento y desayuno'), ('PC', 'Pensión completa')], default='NE', help_text='Régimen', max_length=2)),
                ('reservado', models.CharField(blank=True, choices=[('R', 'Reservado'), ('N', 'No reservado')], default='N', help_text='Reservado', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('comentarios', models.CharField(blank=True, max_length=1000)),
                ('recibida', models.DateField()),
                ('registrada', models.DateField()),
                ('status', models.CharField(blank=True, choices=[('d', 'En duda'), ('n', 'No recibe respuesta'), ('p', 'Pendiente'), ('r', 'Respondida'), ('R', 'Reservada')], default='p', help_text='Estado de la solicitud', max_length=1)),
                ('cotizacionSA', models.FloatField(blank=True, default=0)),
                ('cotizacionHAB', models.FloatField(blank=True, default=0)),
                ('cotizacionAD', models.FloatField(blank=True, default=0)),
                ('cotizacionMP', models.FloatField(blank=True, default=0)),
                ('cotizacionPC', models.FloatField(blank=True, default=0)),
                ('agencia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.agencia')),
                ('calendario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.calendar')),
                ('grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.grupo')),
            ],
            options={
                'ordering': ['registrada'],
            },
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentarios', models.CharField(blank=True, max_length=1000)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.grupo')),
                ('solicitud', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.solicitud')),
            ],
        ),
    ]