from django.urls import path, reverse
from leads import views
# from django.conf.urls import include
from .views import *


urlpatterns = [
    # path('leads/', include('leads.urls')),
    path('', home, name='index'),
    
    # SUPERVISOR ----------------
    path('obtener-unidades/', obtener_unidades, name='obtener-unidades'),
    path('obtener-condiciones/',obtener_condiciones, name='obtener-condiciones'),
    path('obtener-filtros/', obtener_filtros, name='obtener-filtros'),
    path('obtener-municipios/', obtener_municipios, name='obtener_municipios'),
    path('obtener-localidades/', obtener_localidades, name='obtener_localidades'),
    path('consultar-datos/', consultar_datos, name='consultar_datos'),
    path('obtener-asesores/', views.obtener_asesores, name='obtener_asesores'),
    path('asignar-asesor/', views.asignar_asesor, name='asignar_asesor'),
    path('obtener_unidades_por_asesorSu/',obtener_unidades_por_asesorSu, name='obtener_unidades_por_asesorSu'),
    # en edición
    path('guardar_consulta/', views.guardar_consulta, name='guardar_consulta'),

    

    #ASESOR ----------------------
    path('obtener_unidades_por_asesor/',obtener_unidades_por_asesor, name='obtener_unidades_por_asesor'),
    path('obtener_unidades_por_asesor/', views.obtener_unidades_por_asesor, name='obtener_unidades_por_asesor'),
    path('actualizar_estado_unidad/', views.actualizar_estado_unidad, name='actualizar_estado_unidad'),


    

]