from django.shortcuts import render, get_object_or_404
from .models import Agencia, Grupo, Solicitud, Calendar, Cotizacion
from .forms import SolicitudForm, GrupoForm, CotizacionForm, ReservaForm
from django.views import generic
from tablib import Dataset
from django.http import HttpResponseRedirect
import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

hoteles=['HCR', 'HCL', 'HM']
def calendarpage(request):

    context={}
    context['grupos'] = Grupo.objects.all()


    #calendarios=Calendar.objects.all()#filtraré el último

    last_update = Calendar.objects.order_by('-updated')[0]
    prueba=last_update.updated-datetime.timedelta(seconds=1)
    context['calendarios'] = Calendar.objects.filter(updated__gt=prueba)

    #reservados       = Grupo.objects.filter(reservado__exact='R')
    #no_reservados    = Grupo.objects.filter(reservado__exact='N')

    context['gruposHCR'] = Grupo.objects.filter(reservado__exact='HCR')
    context['gruposHCL'] = Grupo.objects.filter(reservado__exact='HCL')
    context['gruposHM'] = Grupo.objects.filter(reservado__exact='HM')
    context['gruposquizas'] = Grupo.objects.filter(reservado__exact='CER')
    context['gruposqueno'] = Grupo.objects.filter(reservado__exact='CNR')
    context['gruposnodisp'] = Grupo.objects.filter(reservado__exact='SD')
    context['gruposnoatendidos'] = Grupo.objects.filter(reservado__exact='NA')

    opciones= request.GET



    for a in request.GET:
        context[a]=opciones[a]



    return render(
        request,
        'calendarindex.html',
        context)

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_grupos=Grupo.objects.all().count()
    num_solicitudes=Solicitud.objects.all().count()
    # Libros disponibles (status = 'a')
    num_solicitudes_pendientes=Solicitud.objects.filter(status__exact='p').count()
    num_solicitudes_duda=Solicitud.objects.filter(status__exact='d').count()
    num_agencias=Agencia.objects.count()  # El 'all()' esta implícito por defecto.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_grupos':num_grupos,'num_solicitudes':num_solicitudes,
        'num_solicitudes_pendientes':num_solicitudes_pendientes,'num_solicitudes_duda':num_solicitudes_duda,
        'num_agencias': num_agencias}
    )

def pendientes(request):
    """

    # Genera contadores de algunos de los objetos principales
    num_grupos=Grupo.objects.all().count()
    num_solicitudes=Solicitud.objects.all().count()
    # Libros disponibles (status = 'a')
    """
    num_solicitudes_pendientes=Solicitud.objects.filter(status__exact='p').count()

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_grupos':num_grupos,'num_solicitudes':num_solicitudes,
        'num_solicitudes_pendientes':num_solicitudes_pendientes,'num_solicitudes_duda':num_solicitudes_duda,
        'num_agencias': num_agencias}
    )



def simple_upload(request):
    if request.method == 'POST':
        calendar_resource = CalendarResource()
        dataset = Dataset()
        new_calendar = request.FILES['myfile']

        imported_data = dataset.load(new_calendar.read())
        result = calendar_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            calendar_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')



class CalendarView(generic.ListView):
    model = Grupo
    entrada=Grupo.entrada

    salida=Grupo.salida
    template_name = 'calendarindex.html'

class GrupoListView(generic.ListView):
    model = Grupo
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'listagrupos.html'  # Specify your own template name/location


class SolicitudListView(generic.ListView):
    model = Solicitud
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'listasolicitudes.html'  # Specify your own template name/location


#  NO LO USO, ES EQUIVALENTE A VIEW POSTERIOR!!!!! URL ESTÁ CON #
class InfoGrupoView(generic.DetailView):
    model = Grupo
    template_name = 'detallegrupo.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entrada=Grupo.entrada
        salida=Grupo.salida
        #precios=Calendar.objects.filter(day__range=[entrada, salida])

        #avgprice = precios.annotate(total=Sum('price'))
        context['calendarios'] = Calendar.objects.all()
        context['grupos'] = Grupo.objects.all()
        #context['avgprice'] = avgprice
        context['avgprice'] = Solicitud.avgprice


        #form = SolicitudForm


        #context['form']=form
        return context

def infogrupo(request, pk):
        # dictionary for initial data with
    # field names as keys
    context ={}

    # add the dictionary during initialization
    context["grupo"] = Grupo.objects.get(id = pk)
    context['entrada']=Grupo.entrada
    context['salida']=Grupo.salida

    context['solicitudes']=Solicitud.objects.filter(grupo = context["grupo"])


    context['cotizaciones']= Cotizacion.objects.all()

    for i in context['solicitudes']:

        print(i.pk)
        print(i)
        print(Cotizacion.objects.filter(solicitud = i))
    #precios=Calendar.objects.filter(day__range=[entrada, salida])

    #avgprice = precios.annotate(total=Sum('price'))
    context['calendarios'] = Calendar.objects.all()
    context['grupos'] = Grupo.objects.all()

    context['gruposHCR'] = Grupo.objects.filter(reservado='HCR')
    context['gruposHCL'] = Grupo.objects.filter(reservado='HCL')
    context['gruposHM'] = Grupo.objects.filter(reservado='HM')
    context['gruposquizas'] = Grupo.objects.filter(reservado='CER')
    context['gruposqueno'] = Grupo.objects.filter(reservado='CNR')
    context['gruposnodisp'] = Grupo.objects.filter(reservado='SD')
    context['gruposnoatendidos'] = Grupo.objects.filter(reservado='NA')

    context['solicitudes_reservadas']   =context['solicitudes'].filter(status__exact='R')
    context['solicitudes_quizas']       =context['solicitudes'].filter(status__exact='r')
    context['solicitudes_nointeresados']=context['solicitudes'].filter(status__exact='d')
    context['solicitudes_pendientes']   =context['solicitudes'].filter(status__exact='p')
    context['solicitudes_sin_disp']     =context['solicitudes'].filter(status__exact='n')
    context['solicitudes_anuladas']     =context['solicitudes'].filter(status__exact='A')

    context['num_solicitudes_reservadas']   =context['solicitudes_reservadas'].count()
    context['num_solicitudes_quizas']       =context['solicitudes_quizas'].count()
    context['num_solicitudes_nointeresados']=context['solicitudes_nointeresados'].count()
    context['num_solicitudes_pendientes']   =context['solicitudes_pendientes'].count()
    context['num_solicitudes_sin_disp']     =context['solicitudes_sin_disp'].count()
    context['num_solicitudes_anuladas']     =context['solicitudes_anuladas'].count()

    #context['avgprice'] = avgprice
    context['avgprice'] = Solicitud.avgprice

    context['color'] = request.GET.get('color')

    opciones= request.GET

    #aver = [x for x in request.GET.values()]

    for a in request.GET:
        context[a]=opciones[a]


    return render(request, "detallegrupo.html", context)

#como infogrupo, pero añade formulario para solicitud
#(!) duplica mucho código (es igual que infogrupo), seguro que se puede hacer mejor


def nuevogrupo(request):
    context={}
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        pk=Grupo.objects.last().pk
        return HttpResponseRedirect(reverse("solicitudgrupo",kwargs={'pk': pk}) )
    return render(request, 'nuevogrupo.html', {'form': form})


def solicitudgrupo(request, pk):
        # dictionary for initial data with
    # field names as keys
    context ={}

    # add the dictionary during initialization
    context["grupo"] = Grupo.objects.get(id = pk)
    context['entrada']=Grupo.entrada
    context['salida']=Grupo.salida
    #precios=Calendar.objects.filter(day__range=[entrada, salida])

    #avgprice = precios.annotate(total=Sum('price'))
    context['calendarios'] = Calendar.objects.all()
    context['grupos'] = Grupo.objects.all()
    #context['avgprice'] = avgprice
    context['avgprice'] = Solicitud.avgprice

    grupo = get_object_or_404(Grupo, pk=pk)
    form = SolicitudForm(request.POST or None)


    context['form']=form
    if form.is_valid():
        solicitud = form.save(commit=False)# Don't save it yet
        solicitud.grupo=grupo
        solicitud.save()
        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pk}) )

    return render(request, 'solicitudgrupo.html', context)

def cotizacion(request, pk):
    context={}


    solicitud = get_object_or_404(Solicitud, pk=pk)
    # pass the object as instance in form
    form = CotizacionForm(request.POST or None)
        # save the data from the form and
    # redirect to detail_view
    if form.is_valid():

        cotizacion=form.save(commit=False)
        cotizacion.solicitud=solicitud
        cotizacion.enviada=datetime.datetime.now()
        cotizacion.save()
        hotel=cotizacion.hotel

        #aquí veo si la solicitud está completamente atendida o falta algún hotel
        #(!)esto debería ir fuera, y funcionar también cada vez que altero la solicitud!!!!
        hoteles=[('HCR', solicitud.solicitudHCR),
            ('HM',solicitud.solicitudHM),
            ('HCL',solicitud.solicitudHCL)]

        cotizaciones = Cotizacion.objects.filter(solicitud=solicitud)

        if solicitud.status=='R':
            pass
        else:
            solicitud.status='r'

            for a,b in hoteles:
                if b:
                    if not cotizaciones.filter(hotel=a):
                        solicitud.status='p'


        pkgrupo=solicitud.grupo.pk


        solicitud.save()

        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pkgrupo}) )

    # add form dictionary to context
    context["form"] = form
    return render(request, "cotizacion.html", context)

def reservacotizacion(request, pk):

    context={}
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    form = ReservaForm(request.POST or None, instance=cotizacion)
    context['form']= form



    solicitud = cotizacion.solicitud

    grupo = solicitud.grupo

    if form.is_valid():

        solicitud.status = 'R'
        grupo.reservado = cotizacion.hotel

        pkgrupo=grupo.pk
        cotizacion.reservada=True

        solicitud.save()
        grupo.save()
        form.save()
        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pkgrupo}))

    return render(request, 'reserva.html', context)

    #return HttpResponseRedirect(reverse("reserva",kwargs={'pk': pk}))
        #super(Solicitud, self).save(*args, **kwargs)
        #return reverse('detallegrupo', kwargs={ 'pk': pk})
        #return super(Solicitud, self).save(*args, **kwargs)
        #context={}

        #return render(request, "reserva.html", context)

def warnings(request):

    context={}
    last_update = Calendar.objects.order_by('-updated')[0]
    margen=last_update.updated-datetime.timedelta(seconds=10)
    last_calendar = Calendar.objects.filter(updated__gt=margen)


    warnings=[]
    bajoprecio = []
    abrirext = []


    HCR={'hotel':'HCR'}
    HM={'hotel':'HM'}
    HCL={'hotel':'HCL'}


    k=1
    hoteles= [HCR, HCL, HM]
    for calendar in last_calendar:

        diasrestantes = (calendar.day - timezone.now().date()).days


        #¿competencia está cerrando?
        abiertos3stars=2
        if calendar.NHprice ==0:
            abiertos3stars-=1
        if calendar.FyGprice ==0:
            abiertos3stars-=1

        #----COMPARACIONES AQUÍ----
        #abierto
        #me preocupa: mucha ocupación, ocupación acelerando, precio muy distinto, cambio brusco en precios competencia
        HCR['price']=calendar.HCRprice
        HCR['rooms']=calendar.HCRrooms
        HCL['price']=calendar.HCLprice
        HCL['rooms']=calendar.HCLrooms
        HM['price']=calendar.HMprice
        HM['rooms']=calendar.HMrooms



        for hotel in hoteles:


            #-----CONDICIONES AQUÍ-----
            #ocupacion
            vacio=hotel['rooms'] <= 75 #(!)poner en función de la capacidad del hotel
            amedias= 75 < hotel['rooms'] <= 30
            bastantelleno = 30 < hotel['rooms'] <= 10
            ultimas= 10 < hotel['rooms'] <= 5

            bajoplaza = hotel['price'] < calendar.precio3stars*0.875

            #esteaño = calendar.day < datetime.date(year=2022,month=1,day=1)
            compcerrada = abiertos3stars == 0

            if hotel['price'] !=0: #abiertos


                if compcerrada and esteaño and not vacio: #competencia cerrada y nosotros abiertos
                    hotel["aviso{0}".format(k)] = '%s: ¿Subir precio? Competencia cerrada. Habs: %s Precio: %s' % (
                        calendar.day,
                        hotel['rooms'],
                        hotel['price'])
                        #(!)estudiar cuatro estrellas
                        #(!)estudiar años anteriores
                    k+=1



                if bajoplaza:
                    print('ey') #competencia abierta pero a precios superiores a los nuestros
                    descuento = str(round(((1-hotel['price']/calendar.precio3stars)*100),2))+'%'
                    #formatday = formatday()
                    hotel["aviso{0}".format(k)] = '%s: ¿Subir precio? Precio inferior a plaza (-%s) %s: %s NH:%s FyG:%s Plaza:%s Habitaciones:%s Incremento:' % (calendar.day,
                        descuento,
                        hotel['hotel'],
                        hotel['price'],
                        calendar.NHprice,
                        calendar.FyGprice,
                        round(calendar.precio3stars,2),
                        hotel['rooms'])
                    print(hotel["aviso{0}".format(k)])
                    k+=1

            #cerrado
            else:
                #cerrado con ocupación baja


                """
                unmes = calendar.day < timezone.now()+datetime.timedelta(months=1)
                unasemana = calendar.day < timezone.now()+datetime.timedelta(weeks=1)
                tresdias = calendar.day < timezone.now()+datetime.timedelta(days=2)
                mañana = calendar.day < timezone.now()+datetime.timedelta(days=1)
                hoy = calendar.day == timezone.now()
                """
                #más fácil


                condiciones= vacio or amedias and diasrestantes <= 30 or bastantelleno and diasrestantes <= 10 or ultimas and diasrestantes <=3

                if condiciones: #quedan muchas habitaciones para el tiempo que falta
                    hotel["aviso{0}".format(k)] = '%s: (%s días) Habs: %s Precio:%s NH:%s FyG:%s' % (
                    calendar.day,
                    diasrestantes,
                    hotel['rooms'],
                    hotel['price'],
                    calendar.NHprice,
                    calendar.FyGprice)
                    k+=1

    context['bajoprecio']=bajoprecio


    print(list(HCL.values())[3:])
    context['HCL']=list(HCL.values())[3:]
    context['HCR']=list(HCR.values())[3:]
    context['HM']=list(HM.values())[3:]



    return render(request, "warnings.html", context)
