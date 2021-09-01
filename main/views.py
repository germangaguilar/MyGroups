from django.shortcuts import render, get_object_or_404
from .models import Agencia, Grupo, Solicitud, Calendar
from .forms import SolicitudForm, GrupoForm, CotizacionForm
from django.views import generic
from tablib import Dataset
from django.http import HttpResponseRedirect
import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse

def calendarpage(request):
    grupos = Grupo.objects.all()


    calendarios=Calendar.objects.all()#filtraré el último

    reservados       = Grupo.objects.filter(reservado__exact='R')
    no_reservados    = Grupo.objects.filter(reservado__exact='N')

    return render(
        request,
        'calendarindex.html',
        context={'grupos':grupos, 'calendarios': calendarios})

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
    #precios=Calendar.objects.filter(day__range=[entrada, salida])

    #avgprice = precios.annotate(total=Sum('price'))
    context['calendarios'] = Calendar.objects.all()
    context['grupos'] = Grupo.objects.all()
    #context['avgprice'] = avgprice
    context['avgprice'] = Solicitud.avgprice



    return render(request, "detallegrupo.html", context)

#como infogrupo, pero añade formulario para solicitud
#(!) duplica mucho código (es igual que infogrupo), seguro que se puede hacer mejor
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

def nuevogrupo(request):
    context={}
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        pk=Grupo.objects.last().pk
        return HttpResponseRedirect(reverse("solicitudgrupo",kwargs={'pk': pk}) )
    return render(request, 'nuevogrupo.html', {'form': form})

def nuevasolicitud(request, pk):
    context={}
    obj = get_object_or_404(Grupo, pk=pk)
    form = SolicitudForm(request.POST or None, instance = obj)
    return render(request, 'detallegrupo.html', {'form': form})

def cotizacion(request, pk):
    context={}


    obj = get_object_or_404(Solicitud, pk=pk)
    # pass the object as instance in form
    form = CotizacionForm(request.POST or None, instance = obj)

        # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        obj.status = 'r'
        pkgrupo=obj.grupo.pk
        form.save()
        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pkgrupo}) )

    # add form dictionary to context
    context["form"] = form
    return render(request, "cotizacion.html", context)

def reservasolicitud(request, pk):
        solicitud = get_object_or_404(Solicitud, pk=pk)
        solicitud.status='R'
        solicitud.save()
        pk=solicitud.grupo.pk

        grupo = get_object_or_404(Grupo, pk=pk)
        #grupo = Grupo.objects.get(pk=pk)

        grupo.reservado = 'R'  # change field
        grupo.save() # this will update only
        return HttpResponseRedirect(reverse("detallegrupo",kwargs={'pk': pk}))
        #super(Solicitud, self).save(*args, **kwargs)
        #return reverse('detallegrupo', kwargs={ 'pk': pk})
        #return super(Solicitud, self).save(*args, **kwargs)
        #context={}

        #return render(request, "reserva.html", context)

def warnings(request):
    context={}
    last_update = Calendar.objects.order_by('-updated')[0]
    prueba=last_update.updated-datetime.timedelta(seconds=1)
    last_calendar = Calendar.objects.filter(updated__gt=prueba)
    # it might be a good idea to inspect the result at this point
    # to ensure you are deleting the right stuff

    warnings=[]
    bajoprecio = []
    abrirext = []





    for calendar in last_calendar:
        print(calendar)
        print(bajoprecio)
        #-----CONDICIONES AQUÍ-----
        #ocupacion
        vacio=calendar.rooms <= 60
        amedias= 60 < calendar.rooms <= 30
        bastantelleno = 30 < calendar.rooms <= 10
        ultimas= 10 < calendar.rooms <= 5

        #precio
        bajoplaza = calendar.price < calendar.precio3stars*0.875

        #¿competencia está cerrando?
        abiertos=2
        if calendar.NHprice ==0:
            abiertos-=1
        if calendar.FyGprice ==0:
            abiertos-=1

        #----COMPARACIONES AQUÍ----
        #abierto
        #me preocupa: mucha ocupación, ocupación acelerando, precio muy distinto, cambio brusco en precios competencia
        if calendar.price != 0:

            #competencia cerrada y nosotros abiertos
            if abiertos == 0:
                bajoprecio.append(
                    '%s: Competencia cerrada. Habs: %s Precio: %s' % (
                    calendar.day,
                    calendar.rooms,
                    calendar.price))
                    #(!)estudiar cuatro estrellas
                    #(!)estudiar años anteriores



            if bajoplaza:
                descuento = str(round(((1-calendar.price/calendar.precio3stars)*100),2))+'%'
                #formatday = formatday()
                bajoprecio.append(
                    '%s: (-%s) HCL: %s NH:%s FyG:%s Plaza:%s Habitaciones:%s Incremento:' % (calendar.day,
                    descuento,
                    calendar.price,
                    calendar.NHprice,
                    calendar.FyGprice,
                    calendar.precio3stars,
                    calendar.rooms))

        #cerrado
        else:
            #cerrado con ocupación baja
            vacio=calendar.rooms <= 60
            amedias= 60 < calendar.rooms <= 30
            bastantelleno = 30 < calendar.rooms <= 10
            ultimas= 10 < calendar.rooms <= 5

            """
            unmes = calendar.day < timezone.now()+datetime.timedelta(months=1)
            unasemana = calendar.day < timezone.now()+datetime.timedelta(weeks=1)
            tresdias = calendar.day < timezone.now()+datetime.timedelta(days=2)
            mañana = calendar.day < timezone.now()+datetime.timedelta(days=1)
            hoy = calendar.day == timezone.now()
            """
            #más fácil
            diasrestantes = (calendar.day - timezone.now().date()).days

            condiciones= vacio or amedias and diasrestantes <= 30 or bastantelleno and diasrestantes <= 10 or ultimas and diasrestantes <=3

            if condiciones:
                abrirext.append('%s: (%s días) Habs: %s Precio:%s NH:%s FyG:%s' % (calendar.day,
                diasrestantes,
                calendar.rooms,
                calendar.price,
                calendar.NHprice,
                calendar.FyGprice))

    context['bajoprecio']=bajoprecio


    print(bajoprecio)
    print(abrirext)


    return render(request, "warnings.html", context)
