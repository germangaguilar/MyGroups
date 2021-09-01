from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Requerida para las instancias de libros únicos
import datetime
import numpy as np

from django.utils import timezone

class Solicitud(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para esta solicitud")
    title = models.CharField(blank=True, max_length=100)
    grupo = models.ForeignKey('Grupo', on_delete=models.SET_NULL, null=True)
    agencia = models.ForeignKey('Agencia', on_delete=models.SET_NULL, null=True)
    calendario      = models.ForeignKey('Calendar', on_delete=models.SET_NULL, null=True, blank=True)
    comentarios     = models.CharField(max_length=1000,blank=True)
    recibida = models.DateField()
    registrada = models.DateField()
    #avgprice = models.FloatField(blank=True)

    """
    HCRavgprice = models.FloatField(blank=True)
    HCLavgprice = models.FloatField(blank=True)
    HMavgprice  = models.FloatField(blank=True)
    """

    LOAN_STATUS = (
        ('d', 'En duda'),
        ('n', 'No recibe respuesta'),
        ('p', 'Pendiente'),
        ('r', 'Respondida'),
        ('R', 'Reservada')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='p', help_text='Estado de la solicitud')

    cotizacionSA    = models.FloatField(default= 0, blank=True)
    cotizacionHAB   = models.FloatField(default= 0, blank=True)
    cotizacionAD    = models.FloatField(default= 0, blank=True)
    cotizacionMP    = models.FloatField(default= 0, blank=True)
    cotizacionPC    = models.FloatField(default= 0, blank=True)

    class Meta:
        ordering = ["registrada"]

    def avgprice(self):
        entrada=self.grupo.entrada
        salida=self.grupo.salida
        calendario = self.calendario

        last_update = Calendar.objects.order_by('-updated')[0]
        prueba=last_update.updated-datetime.timedelta(seconds=1)
        last_calendar = Calendar.objects.filter(updated__gt=prueba)
        # it might be a good idea to inspect the result at this point
        # to ensure you are deleting the right stuff



        dias=last_calendar.filter(day__range=[entrada, salida])
        prices=[]
        for dia in dias:
            prices.append(dia.price)

        avgprice=np.mean(prices)

        return avgprice



    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.grupo.title)

    """
    def get_absolute_url(self):

        return reverse('solicitud', args=[str(self.id)])
    """

    def save(self, *args, **kwargs):

        #self.avgprice = self.avgprice(self)
        return super(Solicitud, self).save(*args, **kwargs)

    def get_absolute_url(self):
        print(str(self.id))
        return reverse('detallesolicitud', kwargs={ 'pk': str(self.id)})


class Grupo(models.Model):


    title = models.CharField(max_length=400)

    #author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    entrada=models.DateField()
    salida =models.DateField()
    pax    =models.IntegerField(default=0, blank=True)
    dobles =models.IntegerField(default=0, blank=True)
    triples=models.IntegerField(default=0, blank=True)
    DUIs   =models.IntegerField(default=0, blank=True)
    singles=models.IntegerField(default=0, blank=True)
    comentarios = models.TextField(default="",max_length=1000, blank=True,help_text="Comentarios adicionales")

    REGIMEN_STATUS = (
        ('NE', 'No especificado'),
        ('SA', 'Solo alojamiento'),
        ('MP', 'Media pensión'),
        ('AD', 'Alojamiento y desayuno'),
        ('PC', 'Pensión completa'),
    )

    regimen = models.CharField(max_length=2, choices=REGIMEN_STATUS, blank=True, default='NE', help_text='Régimen')

    BOOKING_STATUS = (
        ('R', 'Reservado'),
        ('N', 'No reservado'),
    )

    reservado = models.CharField(max_length=1, choices=BOOKING_STATUS, blank=True, default='N', help_text='Reservado')


    def __str__(self):
        """
        String que representa al objeto Book
        """
        return '%s (%s,%s,%s)' % (self.id,self.entrada,self.salida, self.title)

    def formatentrada(self):
        year=str(self.entrada.year)
        month='0'+str(self.entrada.month) if self.entrada.month<10 else str(self.entrada.month)
        day='0'+str(self.entrada.day) if self.entrada.day<10 else str(self.entrada.day)
        date=year+'-'+month+'-'+day
        return date

    def formatsalida(self):
        year=str(self.salida.year)
        month='0'+str(self.salida.month) if self.salida.month<10 else str(self.salida.month)
        day='0'+str(self.salida.day) if self.salida.day<10 else str(self.salida.day)
        date=year+'-'+month+'-'+day
        return date


    def get_absolute_url(self):

        return reverse('detallegrupo', kwargs={ 'pk': str(self.id)})


    def save(self, *args, **kwargs):


        super(Grupo, self).save(*args, **kwargs)
        #return '%s' % (self.noche)

class Cotizacion(models.Model):
    solicitud       = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    grupo           = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    comentarios     = models.CharField(max_length=1000,blank=True)

class Agencia(models.Model):
    """
    Modelo que representa una agencia
    """

    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.nombre


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('agency-detail', args=[str(self.id)])



class Calendar(models.Model):
    day = models.DateField()
    price = models.IntegerField(blank=True)
    FyGprice = models.IntegerField(default=0, blank=True)
    NHprice = models.IntegerField(default=0, blank=True)
    rooms = models.IntegerField(blank=True)
    updated=models.DateTimeField()
    precio3stars=models.FloatField(blank=True)


    def formatday(self):
        year    =   str(self.day.year)
        month   ='0'+str(self.day.month) if self.day.month<10 else str(self.day.month)
        day     ='0'+str(self.day.day)   if self.day.day<10 else str(self.day.day)
        date    = year+'-'+month+'-'+day
        return date

    def dayprice(self):
        price=str(self.price)
        rooms=str(self.rooms)
        dayprice = rooms+' '+price+'€'
        return dayprice

    def warnme(self):
        last_update = Calendar.objects.order_by('-updated')[0]
        prueba=last_update.updated-datetime.timedelta(seconds=1)
        last_calendar = Calendar.objects.filter(updated__lt=prueba)
        # it might be a good idea to inspect the result at this point
        # to ensure you are deleting the right stuff

        warnings=[]
        bajoprecio = []



        if self.price < self.precio3stars*0.9:
            descuento = str((1-self.price/self.precio3stars)*100)+'%'
            #formatday = formatday()
            bajoprecio.append(
                '%s: (-%s) CdL: %s NH:%s FyG:%s Plaza:%s' % (self.day,
                descuento,
                self.price,
                self.NHprice,
                self.FyGprice,
                self.precio3stars))

        print(bajoprecio)
        return bajoprecio

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s %s %s (%s)' % (self.day,self.rooms, self.price,self.updated)

    def save(self, *args, **kwargs):

        self.updated = timezone.now()

        if self.FyGprice >0 and self.NHprice >0:
            self.precio3stars = (self.FyGprice + self.NHprice)/2
        elif self.FyGprice ==0 and self.NHprice >0:
            self.precio3stars = self.NHprice
        elif self.NHprice ==0 and self.FyGprice >0:
            self.precio3stars = self.FyGprice
        else:
            self.precio3stars = 0

        return super(Calendar, self).save(*args, **kwargs)
