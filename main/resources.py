from import_export import resources
from .models import Calendar

class CalendarResource(resources.ModelResource):
    class Meta:
        model = Calendar
