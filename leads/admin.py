from django.contrib import admin
from .models import * 
from import_export.admin import ImportExportMixin

# Register your models here.

class EmpresaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display =['nombreEmp','giro', 'direccionEmp']
    search_fields=['nombreEmp']
    list_per_page = 10

class SucursalAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=['nombreSuc','direccionSuc','empresa']
    search_fields=['nombreSuc']
    list_per_page=10

class SupervisorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=['nomSuper','sucursal']
    search_fields=['nomSuper']
    list_per_page=10

class AsesorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=['nomAses','rutaAses','supervisor']
    search_fields=['nomAses']
    list_per_page=10

class UniEconomicasAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=['id_Uni',
                  'CleeUni',
                  'Nombre_de_la_Unidad_Economica',
                  'Razon_social',
                  'Nombre_de_clase_de_la_actividad',
                  'Descripcion_estrato_personal_ocupado',
                  'Nombre_de_la_vialidad',
                  'Numero_exterior_o_kilometro',
                  'Letra_exterior',
                  'Nombre_de_asentamiento_humano',
                  'Codigo_postal',
                  'Entidad_federetiva',
                  'Municipio',
                  'Localidad',
                  'Numero_de_telefono',
                  'Correo_electronico',
                  'Sitio_en_Internet',
                  'Latitud',
                  'Longitud',
                  'Fecha_de_incorporacion_al_denue'
                  ]
    search_fields=['nom_uniEc','clase_uniEc']
    list_per_page=10

class ConsultaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=['nom_Cons','fecha_Cons','asesor','uniEc']
    search_fields=['nomCons']
    list_per_page=10


admin.site.site_header = 'Administración MLM'
admin.site.index_title = 'Panel de control de MLM'
admin.site.site_title = 'Leads'

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Asesor, AsesorAdmin)
admin.site.register(UniEconomicas, UniEconomicasAdmin)
admin.site.register(Consulta, ConsultaAdmin)
