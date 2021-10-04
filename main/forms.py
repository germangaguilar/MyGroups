from django.forms import ModelForm, TextInput
from .models import Grupo, Solicitud, Cotizacion, Agencia
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
import datetime



class GrupoForm(ModelForm):

    class Meta:
        model = Grupo
        fields = [ 'title','entrada', 'salida', 'pax', 'triples', 'DUIs', 'singles', 'comentarios', 'NE','SA','AD','MP','PC']
        widgets = {
            'entrada': AdminDateWidget(),
            'salida': AdminDateWidget(),
            'title': TextInput(attrs={
                    'placeholder': 'Nombre (opcional)'
                    })
            }
    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get("entrada")
        salida = cleaned_data.get("salida")

        if salida <= entrada:
            raise ValidationError(
                "¡Error! La fecha de salida no puede ser igual o anterior a la fecha de entrada."
            )

        elif salida - entrada > datetime.timedelta(weeks=2):
            raise ValidationError(
                "¡Error! No se admiten grupos de más de dos semanas."
            )



class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['title','agencia', 'recibida', 'registrada', 'solicitudHM','solicitudHCL','solicitudHCR', 'comentarios', 'correo', 'asuntocorreo']
        widgets = {
            'recibida': AdminDateWidget(),
            'registrada': AdminDateWidget(),
            'correo': TextInput(attrs={
                    'style': 'width: 600px; height: 400px;',
                    'placeholder': 'Cuerpo'
                    }),
            'asuntocorreo': TextInput(attrs={
                    'style': 'width: 550px',
                    'placeholder': 'Asunto'
                    }),
            }

        """'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                })
        }"""




class CotizacionForm(ModelForm):
    class Meta:
      model = Cotizacion
      fields = ['disponibilidad','cotizacionSA', 'cotizacionAD', 'cotizacionMP', 'cotizacionPC', 'cotizacionHAB','hotel']


class AgenciaForm(ModelForm):
    class Meta:
      model = Agencia
      fields = ['nombre']



class SinDisponibilidadForm(ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['disponibilidad']


class ReservaForm(ModelForm):
    class Meta:
        model = Cotizacion
        fields= ['num_reserva']
