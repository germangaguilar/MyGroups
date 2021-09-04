from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Requerida para las instancias de libros únicos
import datetime
import numpy as np

from django.utils import timezone

hoteles=['HCR', 'HCL', 'HM', 'NE']

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
        ('d', 'Cotizada pero no va a reservar'),
        ('n', 'Sin disponibilidad'),
        ('p', 'Pendiente'),
        ('r', 'Cotizada, podría reservar'),
        ('R', 'Reservada (borrar)'),
        ('A', 'Reservada y anulada')
    )

    solicitudHCR=models.BooleanField(default=False)
    solicitudHCL=models.BooleanField(default=False)
    solicitudHM=models.BooleanField(default=False)



    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='p', help_text='Estado de la solicitud')




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
        HCLprices=[]
        HMprices=[]
        HCRprices=[]
        for dia in dias:
            HCLprices.append(dia.HCLprice)
            HMprices.append(dia.HMprice)
            HCRprices.append(dia.HCRprice)

        avgHCLprice=np.mean(HCLprices)
        avgHMprice =np.mean(HMprices)
        avgHCRprice=np.mean(HCRprices)

        context={'avgHCLprice': avgHCLprice, 'avgHMprice': avgHMprice, 'avgHCRprice': avgHCRprice}

        avgprices=[x for x in context.values()]

        return avgprices



    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.title)

    """
    def get_absolute_url(self):

        return reverse('solicitud', args=[str(self.id)])
    """

    def save(self, *args, **kwargs):

        #self.avgprice = self.avgprice(self)
        return super(Solicitud, self).save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse('detallesolicitud', kwargs={ 'pk': str(self.id)})

    def reserva_url(self):

        return reverse('reservasolicitud', kwargs={ 'pk': str(self.id)})


class Cotizacion(models.Model):
    solicitud=models.ForeignKey('Solicitud', on_delete=models.SET_NULL, null=True)

    cotizacionSA    = models.FloatField(default= 0, blank=True)
    cotizacionHAB   = models.FloatField(default= 0, blank=True)
    cotizacionAD    = models.FloatField(default= 0, blank=True)
    cotizacionMP    = models.FloatField(default= 0, blank=True)
    cotizacionPC    = models.FloatField(default= 0, blank=True)

    num_reserva = models.CharField(default= '', blank=True, max_length=20)

    HOTELES = (
        ('HCR', 'Hotel Carlton Rioja'),
        ('HCL', 'Hotel Ciudad de Logroño'),
        ('HM', 'Hotel Murrieta'),
        )

    hotel = models.CharField(max_length=3, choices=HOTELES, default='HM', help_text='Hotel que envía la solicitud',blank=True)

    enviada=models.DateTimeField(blank=True, null=True)
    reservada=models.BooleanField(default=False)





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

    NE=models.BooleanField()
    SA=models.BooleanField()
    AD=models.BooleanField()
    MP=models.BooleanField()
    PC=models.BooleanField()

    enviada=models.DateField(default=datetime.date.today)

    """
    REGIMEN_STATUS = (
        ('NE', 'No especificado'),
        ('SA', 'Solo alojamiento'),
        ('MP', 'Media pensión'),
        ('AD', 'Alojamiento y desayuno'),
        ('PC', 'Pensión completa'),
    )

    regimen = models.CharField(max_length=2, choices=REGIMEN_STATUS, blank=True, default='NE', help_text='Régimen')"""

    BOOKING_STATUS = (
        ('HCR', 'Reservado en HCR'),
        ('HCL', 'Reservado en HCL'),
        ('HM', 'Reservado en HM'),
        ('CER', 'Cotizado, esperando respuesta'),
        ('CNR', 'Cotizado, no reserva'),
        ('SD', 'Sin disponibilidad'),
        ('NA', 'No atendido')
    )

    reservado = models.CharField(max_length=3, choices=BOOKING_STATUS, blank=True, default='NA', help_text='Estado del grupo')


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

"""class Cotizacion(models.Model):
    solicitud       = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    grupo           = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    comentarios     = models.CharField(max_length=1000,blank=True)"""

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

    HCLprice = models.FloatField(default=0,blank=True)
    HCRprice = models.FloatField(default=0,blank=True)
    HMprice = models.FloatField(default=0,blank=True)
    FyGprice = models.FloatField(default=0, blank=True)
    NHprice = models.FloatField(default=0, blank=True)

    HCLrooms = models.IntegerField(default=0,blank=True)
    HCRrooms = models.IntegerField(default=0,blank=True)
    HMrooms = models.IntegerField(default=0,blank=True)

    HCLrooms_lastupdate=models.IntegerField(default=0,blank=True)
    HCLrooms_lastweek=models.IntegerField(default=0,blank=True)
    HCLrooms_lastmonth=models.IntegerField(default=0,blank=True)

    HCRrooms_lastupdate=models.IntegerField(default=0,blank=True)
    HCRrooms_lastweek=models.IntegerField(default=0,blank=True)
    HCRrooms_lastmonth=models.IntegerField(default=0,blank=True)

    HMrooms_lastupdate=models.IntegerField(default=0,blank=True)
    HMrooms_lastweek=models.IntegerField(default=0,blank=True)
    HMrooms_lastmonth=models.IntegerField(default=0,blank=True)

    HCLprice_lastupdate=models.IntegerField(default=0,blank=True)
    HCLprice_lastweek=models.IntegerField(default=0,blank=True)
    HCLprice_lastmonth=models.IntegerField(default=0,blank=True)

    HCRprice_lastupdate=models.IntegerField(default=0,blank=True)
    HCRprice_lastweek=models.IntegerField(default=0,blank=True)
    HCRprice_lastmonth=models.IntegerField(default=0,blank=True)

    HMprice_lastupdate=models.IntegerField(default=0,blank=True)
    HMprice_lastweek=models.IntegerField(default=0,blank=True)
    HMprice_lastmonth=models.IntegerField(default=0,blank=True)

    FyGprice_lastupdate=models.IntegerField(default=0,blank=True)
    FyGprice_lastweek=models.IntegerField(default=0,blank=True)
    FyGprice_lastmonth=models.IntegerField(default=0,blank=True)

    NHprice_lastupdate=models.IntegerField(default=0,blank=True)
    NHprice_lastweek=models.IntegerField(default=0,blank=True)
    NHprice_lastmonth=models.IntegerField(default=0,blank=True)

    festivo=models.CharField(default='', max_length=30, blank=True)

    updated=models.DateTimeField(blank=True,null=True)
    precio3stars=models.FloatField(blank=True)
    #precio4stars=models.FloatField(blank=True)


    def formatday(self):
        year    =   str(self.day.year)
        month   ='0'+str(self.day.month) if self.day.month<10 else str(self.day.month)
        day     ='0'+str(self.day.day)   if self.day.day<10 else str(self.day.day)
        date    = year+'-'+month+'-'+day
        return date

    def HCLdayprice(self):


        HCLprice=str(int(self.HCLprice))

        HCLrooms=str(self.HCLrooms)

        HCLdayprice = HCLrooms+' '+HCLprice+'€'

        return HCLdayprice

    def HCRdayprice(self):


        HCRprice=str(int(self.HCRprice))

        HCRrooms=str(self.HCRrooms)

        HCRdayprice = HCRrooms+' '+HCRprice+'€'

        return HCRdayprice

    def HMdayprice(self):


        HMprice=str(int(self.HMprice))

        HMrooms=str(self.HMrooms)

        HMdayprice = HMrooms+' '+HMprice+'€'

        return HMdayprice



    def preturrooms(self):

        HCLrooms=str(self.HCLrooms)
        HMrooms=str(self.HMrooms)
        HCRrooms=str(self.HCRrooms)

        rooms = 'HM: '+HMrooms+'h '+'HCL: '+HCLrooms+'h '+'HCR: '+HCRrooms+'h'

        return rooms

    def preturprices(self):

        HCLprice=str(self.HCLprice)
        HMprice=str(self.HMprice)
        HCRprice=str(self.HCRprice)

        price = 'HM: '+HMprice+'€ '+'HCL: '+HCLprice+'€ '+'HCR: '+HCRprice+'€'

        return price




    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.day,self.updated)

    def save(self, *args, **kwargs):

        self.updated = timezone.now()




        dayago=self.updated-datetime.timedelta(hours=12)
        previous_calendars = Calendar.objects.filter(updated__lt=dayago)


        dayago_update = previous_calendars.order_by('-updated')[0]
        margen2=dayago_update.updated-datetime.timedelta(seconds=10)
        dayago_calendar= previous_calendars.filter(updated__gt=margen2)

        day=dayago_calendar.get(day=self.day)

        self.HCLrooms_lastupdate=self.HCLrooms - day.HCLrooms
        self.HCRrooms_lastupdate=self.HCRrooms - day.HCRrooms
        self.HMrooms_lastupdate=self.HMrooms - day.HMrooms

        self.HCLprice_lastupdate=self.HCLprice - day.HCLprice
        self.HCRprice_lastupdate=self.HCRprice - day.HCRprice
        self.HMprice_lastupdate=self.HMprice - day.HMprice

        self.FyGprice_lastupdate=self.FyGprice - day.FyGprice
        self.NHprice_lastupdate=self.NHprice - day.NHprice


        weekago=self.updated-datetime.timedelta(days=6)
        previous_calendars = Calendar.objects.filter(updated__lt=weekago)


        weekago_update = previous_calendars.order_by('-updated')[0]
        margen2=weekago_update.updated-datetime.timedelta(seconds=10)
        weekago_calendar= previous_calendars.filter(updated__gt=margen2)

        week=weekago_calendar.get(day=self.day)

        self.HCLrooms_lastweek=self.HCLrooms - week.HCLrooms
        self.HCRrooms_lastweek=self.HCRrooms - week.HCRrooms
        self.HMrooms_lastweek=self.HMrooms - week.HMrooms

        self.HCLprice_lastweek=self.HCLprice - week.HCLprice
        self.HCRprice_lastweek=self.HCRprice - week.HCRprice
        self.HMprice_lastweek=self.HMprice - week.HMprice

        self.FyGprice_lastweek=self.FyGprice - week.FyGprice
        self.NHprice_lastweek=self.NHprice - week.NHprice


        monthago=self.updated-datetime.timedelta(days=6)
        previous_calendars = Calendar.objects.filter(updated__lt=monthago)


        monthago_update = previous_calendars.order_by('-updated')[0]
        margen2=monthago_update.updated-datetime.timedelta(seconds=10)
        monthago_calendar= previous_calendars.filter(updated__gt=margen2)

        month=monthago_calendar.get(day=self.day)

        self.HCLrooms_lastmonth=self.HCLrooms - month.HCLrooms
        self.HCRrooms_lastmonth=self.HCRrooms - month.HCRrooms
        self.HMrooms_lastmonth=self.HMrooms - month.HMrooms

        self.HCLprice_lastmonth=self.HCLprice - month.HCLprice
        self.HCRprice_lastmonth=self.HCRprice - month.HCRprice
        self.HMprice_lastmonth=self.HMprice - month.HMprice

        self.FyGprice_lastmonth=self.FyGprice - month.FyGprice
        self.NHprice_lastmonth=self.NHprice - month.NHprice



        if self.FyGprice >0 and self.NHprice >0:
            if self.FyGprice > self.NHprice *1.2:
                self.precio3stars = self.NHprice *1.2
            else:
                self.precio3stars = (self.FyGprice + self.NHprice)/2
        elif self.FyGprice ==0 and self.NHprice >0:
            self.precio3stars = self.NHprice
        elif self.NHprice ==0 and self.FyGprice >0:
            self.precio3stars = self.FyGprice
        else:
            self.precio3stars = 0

        return super(Calendar, self).save(*args, **kwargs)
