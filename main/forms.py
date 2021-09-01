from django.forms import ModelForm
from .models import Grupo, Solicitud
from django.contrib.admin.widgets import AdminDateWidget


class GrupoForm(ModelForm):

    class Meta:
        model = Grupo
        fields = ['title', 'entrada', 'salida', 'pax', 'triples', 'DUIs', 'singles', 'comentarios', 'NE','SA','AD','MP','PC']
        widgets = {
            'entrada': AdminDateWidget(),
            'salida': AdminDateWidget(),
            }
class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['title','agencia', 'recibida', 'registrada']
        widgets = {
            'recibida': AdminDateWidget(),
            'registrada': AdminDateWidget(),
            }

class CotizacionForm(ModelForm):
    class Meta:
      model = Solicitud
      fields = ['cotizacionSA', 'cotizacionAD', 'cotizacionMP', 'cotizacionPC', 'cotizacionHAB']
