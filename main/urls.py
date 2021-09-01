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
    url("calendario2", views.CalendarView.as_view(), name='calendarpage2'),
    path("calendario<hotel>", views.calendarpage, name='calendarpage2'),
    url("nuevogrupo", views.nuevogrupo, name='nuevogrupo'),
    url("detallegrupo(?P<pk>\d+)$", views.infogrupo, name='detallegrupo'),
    url("solicitudgrupo(?P<pk>\d+)$", views.solicitudgrupo, name='solicitudgrupo'), #crea solicitud
    url("detallesolicitud(?P<pk>\d+)$", views.cotizacion, name='detallesolicitud'), #cotización para solicitud
    url("reservasolicitud(?P<pk>\d+)$", views.reservasolicitud, name='reservasolicitud'),    #confirma reserva solicitud
    url("warnings", views.warnings, name='warnings'),
]
