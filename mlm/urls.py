"""
URL configuration for mlm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from leads import views



urlpatterns = [
    path('leads/', include('leads.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.home, name='home'),
    path('login/', views.signin, name='login'),
    path('salir/', views.salir, name='salir'),

    # SUPERVISOR ------
    path('accion/', views.accion, name='accion'),
    path('consulta1/',views.consulta1, name='consulta1'),
    path('consulta2/', views.consulta2,name='consulta2'),
    path('segConsulta/',views.segConsulta, name='seg_consulta' ),
    path('dash/', views.dash, name='dash'),
    path('verAsesor/', views.verAsesor, name='verAsesor'), #ver asesores y sus unidades asignadas
    path('obtener-unidades/', views.obtener_unidades, name='obtener-unidades'),
    path('obtener-condiciones/',views.obtener_condiciones, name='obtener-condiciones'),
    path('obtener-filtros/', views.obtener_filtros, name='obtener-filtros'),
    path('obtener-municipios/', views.obtener_municipios, name='obtener_municipios'),
    path('obtener-localidades/', views.obtener_localidades, name='obtener_localidades'),
    path('consultar-datos/', views.consultar_datos, name='consultar_datos'),
    path('obtener-asesores/', views.obtener_asesores, name='obtener_asesores'),
    path('asignar-asesor/', views.asignar_asesor, name='asignar_asesor'),
    path('obtener_unidades_por_asesorSu/', views.obtener_unidades_por_asesorSu, name='obtener_unidades_por_asesorSu'),
    

    #ASESORES -------------
    path('accionAses/',views.accionAses, name='accionAses'),
    path('asesorSeg/',views.asesorSeg, name='asesorSeg'),
    path('obtener_unidades_por_asesor/',views.obtener_unidades_por_asesor, name="obtener_unidades_por_asesor"),
    path('obtener_unidades_por_asesor/', views.obtener_unidades_por_asesor, name='obtener_unidades_por_asesor'),
    path('actualizar_estado_unidad/', views.actualizar_estado_unidad, name='actualizar_estado_unidad'),


    

    ]