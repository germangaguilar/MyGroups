from django.shortcuts import render, get_object_or_404
from .models import Agencia, Grupo, Solicitud, Calendar, Cotizacion
from .forms import SolicitudForm, GrupoForm, CotizacionForm, ReservaForm, SinDisponibilidadForm, AgenciaForm
from django.views import generic
from tablib import Dataset
from django.http import HttpResponseRedirect
import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Avg

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


    opciones = request.GET
    for a in   request.GET:
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
    queryset = Grupo.objects.order_by('-registrado')
    paginate_by = 15
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


    #precios=Calendar.objects.filter(day__range=[entrada, salida])

    #avgprice = precios.annotate(total=Sum('price'))
    #context['calendarios'] = Calendar.objects.all()

    last_update = Calendar.objects.order_by('-updated')[0]
    margen=last_update.updated-datetime.timedelta(seconds=10)
    context['calendarios']= Calendar.objects.filter(updated__gt=margen)

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
    formgrupo = GrupoForm(request.POST or None)
    form=SolicitudForm(request.POST or None)


    if formgrupo.is_valid() and form.is_valid():
        grupo=formgrupo.save(commit=False)


        mismaentrada=Grupo.objects.filter(entrada=grupo.entrada)

        if len(mismaentrada) >0:
            mismasalida =mismaentrada.filter(salida=grupo.salida)
            if len(mismasalida) >0:
                margen= grupo.registrado - datetime.timedelta(weeks=2)
                hacepoco=mismasalida.filter(registrado__gt=margen)

                if len(hacepoco)>0:
                    print('MISMO GRUPOOOOOOOO')


        solicitud = form.save(commit=False)

        solicitud.grupo = grupo

        strAD='AD ' if grupo.AD else ''
        strMP='MP ' if grupo.MP else ''
        strPC='PC ' if grupo.PC else ''
        strSA='SA ' if grupo.SA else ''
        strNE='NE ' if grupo.NE else ''

        strRegimen=strNE+strSA+strAD+strMP+strPC

        title = grupo.title+' '+str(grupo.pax)+'pax'+' '+strRegimen+' '+str(solicitud.agencia)

        grupo.reservado='NA'
        grupo.title = title
        #solicitud.grupo = Grupo.objects.last()
        #solicitud.grupo = get_object_or_404(Grupo, pk=grupo.pk)
        grupo.save()
        solicitud.save()
        #pk=Grupo.objects.last().pk

        pk=grupo.pk
        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pk}) )
    return render(request, 'nuevogrupo.html', {'form': form, 'formgrupo':formgrupo})

def modificargrupo(request, pk):

    grupo = get_object_or_404(Grupo, pk=pk)

    form = GrupoForm(request.POST or None, instance=grupo)

    context={}
    context['formgrupo']=form

    grupo = Grupo.objects.get(id = pk)

    context["grupo"]=grupo

    entrada=grupo.entrada
    context['entrada']=entrada

    salida=grupo.salida
    context['salida']=salida

    last_update = Calendar.objects.order_by('-updated')[0]
    margen=last_update.updated-datetime.timedelta(seconds=10)
    calendario= Calendar.objects.filter(updated__gt=margen)
    context['calendarios']=calendario


    calendarioaux=calendario.filter(day__gte=entrada)
    calendariogrupo=calendarioaux.filter(day__lt=salida)

    context['HCLavg'] = list(calendariogrupo.aggregate(Avg('HCLprice')).values())[0]
    context['HCRavg'] = list(calendariogrupo.aggregate(Avg('HCRprice')).values())[0]
    context['HMavg'] = list(calendariogrupo.aggregate(Avg('HMprice')).values())[0]





    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("detallegrupo", kwargs={'pk': pk}) )

    context['bottontext']='Modificar'

    return render(request, "modificargrupo.html", context)


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
    pkgrupo=solicitud.grupo.pk



    grupo = get_object_or_404(Grupo, pk=pkgrupo)
    # pass the object as instance in form
    form = CotizacionForm(request.POST or None)
        # save the data from the form and

    context['solicitud']=solicitud
    context['grupo']=grupo
    context["form"] = form
    # redirect to detail_view


    if form.is_valid():
        print('ey1')
        cotizacion=form.save(commit=False)
        hotel=cotizacion.hotel
        cotizaciones=Cotizacion.objects.filter(solicitud=solicitud)
        cotizacionmismohotel=cotizaciones.filter(hotel=hotel).count()

        if cotizacionmismohotel >= 1:
            viejacotizacion=cotizaciones.get(hotel=hotel)

            if viejacotizacion.pk != cotizacion.pk:
                messages.success(request, "¡El hotel "+str(hotel)+" ya ha enviado una cotización! Puedes modificarla aquí.")
                pk=viejacotizacion.pk
                print('cotizacion')
                print(cotizacion)
                print(pk)
                return HttpResponseRedirect(reverse("cotizacion", kwargs={'pk': pk}) )
            else:
                print('modificando cotizacion')
                pass

        cotizacion.solicitud=solicitud
        cotizacion.enviada=datetime.datetime.now()
        cotizacion.save()

        hoteles=[('HCR', solicitud.solicitudHCR),
            ('HM',solicitud.solicitudHM),
            ('HCL',solicitud.solicitudHCL)]

        cotizaciones = Cotizacion.objects.filter(solicitud=solicitud)

        if solicitud.status=='R':
            pass

        else:

            if cotizacion.disponibilidad==False:
                solicitud.status='n'
                grupo.reservado='SD' if grupo.reservado != 'R'or grupo.reservado != 'CER' else 'R'

            elif cotizacion.disponibilidad==True:
                solicitud.status='r'
                grupo.reservado='CER' if grupo.reservado != 'R' else 'R'

            #aquí veo si la solicitud está completamente atendida o falta algún hotel
            #(!)esto debería ir fuera, y funcionar también cada vez que altero la solicitud!!!!

            for a,b in hoteles:
                if b:
                    if not cotizaciones.filter(hotel=a):
                        solicitud.status='p'
                        grupo.reservado='NA' if grupo.reservado != 'R' else 'R'

        solicitud.save()
        grupo.save()
        print('ey')
        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pkgrupo}) )
    else:
        print('oooh')

    # add form dictionary to context
    context['bottontext']='Registrar'

    return render(request, "cotizacion.html", context)

def modificarcotizacion(request, pk):

    cotizacion = get_object_or_404(Cotizacion, pk=pk)

    form = CotizacionForm(request.POST or None, instance=cotizacion)

    context={}
    context['form']=form
    if form.is_valid():
        form.save()
        grupo=cotizacion.solicitud.grupo
        pk=grupo.pk

        return HttpResponseRedirect(reverse("detallegrupo", kwargs={'pk': pk}) )

    context['bottontext']='Modificar'
    return render(request, "cotizacion.html", context)

def sindisponibilidad(request, pk):
    context={}


    solicitud = get_object_or_404(Solicitud, pk=pk)
    pkgrupo=solicitud.grupo.pk
    grupo = get_object_or_404(Grupo, pk=pkgrupo)

    form = SinDisponibilidadForm(request.POST or None)

    context['form'] = form

    #cotizacion = Cotizacion(name='Beatles Blog', tagline='All the latest Beatles news.')
    #b.save()

    if form.is_valid():

        cotizacion = form.save(commit=False)

        cotizacion.solicitud = solicitud

        cotizaciones = Cotizacion.objects.filter(solicitud=solicitud)
        hoteles=[('HCR', solicitud.solicitudHCR),
            ('HM',solicitud.solicitudHM),
            ('HCL',solicitud.solicitudHCL)]



        if solicitud.status=='R':
            pass
        else:
            solicitud.status='n'
            grupo.reservado='SD' if grupo.reservado != 'R' else 'R'

            for a,b in hoteles:
                if b:
                    if not cotizaciones.filter(hotel=a):
                        solicitud.status='p'
                        grupo.reservado='NA' if grupo.reservado != 'R' else 'R'

        grupo.save()
        solicitud.save()

        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pkgrupo}) )

    return render(request, "sindisponibilidad.html", context)

def nuevaagencia(request):
	form = AgenciaForm(request.POST or None)
	if form.is_valid():
		instance = form.save()
	return render(request, "nuevaagencia.html", {"form" : form})

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

    context['calendario']=last_calendar
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

            if calendar.precio3stars != 0:
                descuento = str(round(((1-hotel['price']/calendar.precio3stars)*100),2))+'%'
            else:
                descuento = '100%'

            #-----CONDICIONES AQUÍ-----
            #ocupacion
            vacio=hotel['rooms'] <= 75 #(!)poner en función de la capacidad del hotel
            amedias= 75 < hotel['rooms'] <= 30
            bastantelleno = 30 < hotel['rooms'] <= 10
            ultimas= 10 < hotel['rooms'] <= 5

            bajoplaza = hotel['price'] < calendar.precio3stars*0.875

            esteaño = calendar.day < datetime.date(year=2022,month=1,day=1)
            compcerrada = abiertos3stars == 0

            if hotel['price'] !=0: #abiertos


                if compcerrada and esteaño and not vacio: #competencia cerrada y nosotros abiertos
                    hotel["aviso{0}".format(k)] = {
                        'dia': calendar.day,
                        'recomendacion': 'Subir precio',
                        'descuento':'+100%'}
                        #(!)estudiar cuatro estrellas
                        #(!)estudiar años anteriores
                    k+=1



                if bajoplaza:
                    #competencia abierta pero a precios superiores a los nuestros

                    #formatday = formatday()
                    hotel["aviso{0}".format(k)] = {
                        'recomendacion':'Subir precio',
                        'dia':calendar.day,
                        'descuento':descuento,}

                    k+=1

            #cerrado
            else:
                #cerrado con ocupación baja

                condiciones= vacio or amedias and diasrestantes <= 30 or bastantelleno and diasrestantes <= 10 or ultimas and diasrestantes <=3

                if condiciones: #quedan muchas habitaciones para el tiempo que falta
                    hotel["aviso{0}".format(k)] = {
                    'recomendacion':'Abrir externo',
                    'dia':calendar.day,
                    'descuento':descuento,}
                    k+=1

    context['bajoprecio']=bajoprecio


    context['HCL']=list(HCL.values())[3:]
    context['HCR']=list(HCR.values())[3:]
    context['HM']=list(HM.values())[3:]

    context['dayswithwarnings']=[]

    for a in context['HCL']+context['HCR']+context['HM']:
        context['dayswithwarnings'].append(a['dia'])

    context['dayswithwarnings'] = list(dict.fromkeys(context['dayswithwarnings']))




    return render(request, "warnings.html", context)

def actualizar(request):
    print('ey')
    hoy = datetime.date.today()
    diezdias= hoy - datetime.timedelta(days=10)
    pendientes=Grupo.objects.filter(reservado='CER')
    noreserva=pendientes.filter(registrado__lt=diezdias)
    print(noreserva)
    for i in noreserva:
        print(i)
        i.reservado='CNR'
        i.save()
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
