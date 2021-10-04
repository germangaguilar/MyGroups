from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url("listagrupos", views.GrupoListView.as_view(), name='listagrupos'),
    url("listasolicitudes", views.SolicitudListView.as_view(), name='listasolicitudes'),
    #url("detallegrupo(?P<pk>\d+)$", views.InfoGrupoView.as_view(), name='detallegrupo'),
    #url("detallegrupo(?P<pk>\d+)$/actualizado", views.InfoGrupoView.as_view(), name='detallegrupo'),
    #url("calendario", views.calendarpage, name='calendarpage'),

    path("calendario2?gruposHCR=gruposHCR", views.calendarpage, name='calendarpage2'),
    path("calendario2", views.calendarpage, name='calendarpage'),
    url("nuevogrupo", views.nuevogrupo, name='nuevogrupo'),
    path("detallegrupo<pk>", views.infogrupo, name='detallegrupo'),
    url("solicitudgrupo(?P<pk>\d+)$", views.solicitudgrupo, name='solicitudgrupo'), #crea solicitud
    url("detallesolicitud(?P<pk>\d+)$", views.cotizacion, name='detallesolicitud'), #cotización para solicitud
    path("reservacotizacion<pk>", views.reservacotizacion, name='reservacotizacion'),    #confirma reserva solicitud
    url("warnings", views.warnings, name='warnings'),
    url("actualizado", views.actualizar, name='actualizar'),
    path("sindisponibilidad<pk>", views.sindisponibilidad, name='sindisponibilidad'),
    path("cotizacion<pk>", views.modificarcotizacion, name='cotizacion'),
    path("modificargrupo<pk>", views.modificargrupo, name='modificargrupo'),
    url("nuevaagencia", views.nuevaagencia, name = "nuevaagencia"),

]
