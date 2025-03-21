from django.urls import path, reverse
from leads import views
from .views import *


urlpatterns = [
    path('', home, name='index'),
    # path('consulta2/', views.consulta2, name='consulta2'),
    path('obtener-unidades/', obtener_unidades, name='obtener-unidades'),
    path('obtener-condiciones/',obtener_condiciones, name='obtener-condiciones'),
    path('obtener-filtros/', obtener_filtros, name='obtener-filtros'),
    path('obtener-municipios/', obtener_municipios, name='obtener_municipios'),
    path('obtener-localidades/', obtener_localidades, name='obtener_localidades'),
    path('consultar-datos/', consultar_datos, name='consultar_datos'),
    path('obtener-asesores/', views.obtener_asesores, name='obtener_asesores'),
    path('obtener-asesores/', obtener_asesores, name='obtener_asesores'),
    path('asignar-asesor/', views.asignar_asesor, name='asignar_asesor'),
    path('obtener_unidades_por_asesor/',obtener_unidades_por_asesor, name='obtener_unidades_por_asesor')
]