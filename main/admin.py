from django.contrib import admin

# Register your models here.
from .models import  Agencia, Grupo, Solicitud, Calendar
from import_export.admin import ImportExportModelAdmin


@admin.register(Calendar)
class CalendarAdmin(ImportExportModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('day', 'HCLrooms', 'HCRrooms', 'HMrooms','HCLprice', 'HCRprice', 'HMprice','updated')
        }),
        ('Competencia', {
            'fields': ('NHprice', 'FyGprice', 'precio3stars')
        }),

    )

admin.site.register(Agencia)

# admin.site.register(Author)
#admin.site.register(Genre)
#admin.site.register(BookInstance)
# Define the admin class





@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_filter = ('status', 'registrada')

    fieldsets = (
        (None, {
            'fields': ('grupo', 'agencia',
            'comentarios')
        }),
        ('Availability', {
            'fields': ('status', 'registrada')
        }),
        ('Cotizacion', {
            'fields': ('cotizacionSA',
                'cotizacionHAB',
                'cotizacionAD',
                'cotizacionMP',
                'cotizacionPC')
        }),

    )



class SolicitudInline(admin.TabularInline):
    model = Solicitud

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    #list_display = ('title', 'author', 'display_genre')
    inlines = [SolicitudInline]
