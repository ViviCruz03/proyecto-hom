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
    path('', include('leads.urls')),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.signin, name='login'),
    path('salir/', views.salir, name='salir'),
    path('accion/', views.accion, name='accion'),
    path('crearConsulta/',views.crearConsulta, name='crear_consulta'),
    path('consulta2/', views.consulta2,name='consulta2'),
    path('segConsulta/',views.segConsulta, name='seg_consulta' ),
    path('dash/', views.dash, name='dash'),
    path('verAsesor/', views.verAsesor, name='verAsesor'),
    path('conAsesor', views.conAsesor, name='conAsesor')
    ]