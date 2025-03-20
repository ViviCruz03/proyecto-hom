from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate #Biblioteca de django que permite crear una coockie para la sesión del usuario
from django.db import IntegrityError
from .models import *  
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
import json





#Pantalla de home
def home (request):
    return render(request, 'index.html')

#Inicio de sesión
def signin (request):
    if request.method == 'GET':
        return render(request, 'login.html',{
        'form': AuthenticationForm
        })
    else:
        user=authenticate (
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'El nombre o la contraseña son incorrectos'
        })
        else:
            login(request, user)
            return redirect('accion')

#Funcion de salir de sesión
@login_required        
def salir(request):
    logout(request)
    return redirect('index')

#Redirigir a la pantalla acción       
@login_required
def accion(request):
    return render(request, 'accion.html')

#Crear consultas a partir de estado, municipio y localidad
@login_required
@user_passes_test(Supervisor)
def crearConsulta(request):
    return render(request, 'consulta1.html')

#Enlista las unidades econónicas
class UniEconomicaListView(ListView):
    model = UniEconomicas
    template_name = 'consulta2.html'
    context_object_name = 'unis'

#Enlistar los asesores
class AsesoresView(ListView):
    model= Asesor
    template_name='consulta1.tml'
    context_object_name = 'asesores'

#Trae las unidades desde la base de datos
def obtener_unidades(request):
    unidades = UniEconomicas.objects.all().values(
        'Nombre_de_la_Unidad_Economica',
        'Nombre_de_clase_de_la_actividad', 
        'Descripcion_estrato_personal_ocupado', 
        'Nombre_de_la_vialidad', 
        'Numero_exterior_o_kilometro', 
        'Letra_exterior', 
        'Codigo_postal',
        'Latitud',
        'Longitud',
        'Fecha_de_incorporacion_al_denue'
        )
    return JsonResponse({'unidades': list(unidades)})

#Filtrar las condiciones de las unidades
def obtener_condiciones(request):
    condiciones = UniEconomicas.objects.values_list('Nombre_de_clase_de_la_actividad', flat=True).distinct()
    # print(f"Condiciones: {condiciones}")
    if condiciones.exists():
        return JsonResponse({'condiciones': list(condiciones)})
    else:
        return JsonResponse({'condiciones':[]}, status=404)

#Filtrar los estados, municipios y localidades
def obtener_filtros(request):
    estados = UniEconomicas.objects.values_list('Entidad_federetiva', flat=True).distinct()
    if estados.exists():
        return JsonResponse({'estados': list(estados)})
    else:
        return JsonResponse({'estados': []}, status=404)

#Devuelve municipios según el estado seleccionado
def obtener_municipios(request):
    estado = request.GET.get('estado', None)
    # print(f"Estado recibido: {estado}")
    if estado:
        # Filtrar los municipios que pertenecen al estado solicitado
        municipios = UniEconomicas.objects.filter(Entidad_federetiva__icontains=estado).values_list('Municipio', flat=True).distinct()
        # print(f"Municipios encontrados: {municipios}")
        return JsonResponse({'municipios': list(municipios)})
    return JsonResponse({'municipios': []})

#Devuelve localidades según el municipio seleccionado
def obtener_localidades(request):
    municipio = request.GET.get('municipio', None)
    # print(f"municipio recibido: {municipio}")
    if municipio:
        # Filtrar las localidades que pertenecen al municipio solicitado
        localidades = UniEconomicas.objects.filter(Municipio__icontains=municipio).values_list('Localidad', flat=True).distinct()
        # print(f"localidades recibidas: {localidades}")
        return JsonResponse({'localidades': list(localidades)})
    return JsonResponse({'localidades': []})

#Realizar la consulta a partir de las condiciones con est, mun, local
def consultar_datos(request):
    # Obtener los parámetros de la solicitud
    condicion = request.GET.get('condicion', '').strip()
    estado = request.GET.get('estado', '').strip()
    municipio = request.GET.get('municipio', '').strip()
    localidad = request.GET.get('localidad', '').strip()

    # Construcción dinámica del filtro
    filtros = {}
    if condicion:
        filtros['Nombre_de_clase_de_la_actividad__icontains'] = condicion
    if estado:
        filtros['Entidad_federetiva__icontains'] = estado
    if municipio:
        filtros['Municipio__icontains'] = municipio
    if localidad:
        filtros['Localidad__icontains'] = localidad

    # Realizar la consulta con los filtros aplicados
    resultados = UniEconomicas.objects.filter(**filtros).values(
        'Nombre_de_la_Unidad_Economica',
        'Nombre_de_clase_de_la_actividad', 
        'Descripcion_estrato_personal_ocupado', 
        'Nombre_de_la_vialidad', 
        'Numero_exterior_o_kilometro', 
        'Letra_exterior', 
        'Codigo_postal',
        'Latitud', 
        'Longitud',
        'Fecha_de_incorporacion_al_denue'
        )

    # Convertir resultados a lista y devolver JSON
    return JsonResponse({'resultados': list(resultados)})


#Obtener los asesores
def obtener_asesores(request):
    # Obtener todos los asesores
    if request.method == 'GET':
        asesores = Asesor.objects.all()
        asesor_data = [{'id': asesor.id, 'nombre': asesor.nomAses} for asesor in asesores]

    return JsonResponse({'asesores': asesor_data})



def asignar_asesor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        asesor_id = data.get('asesor_id')
        unidades = data.get('unidades')

        try:
            asesor = Asesor.objects.get(id=asesor_id)
            for unidad_data in unidades:
                unidad = UniEconomicas.objects.get(Nombre_de_la_Unidad_Economica=unidad_data['Nombre'])
                # Aquí, asignamos el asesor a la unidad (si tienes un campo en UniEconomicas para esto)
                unidad.asesor = asesor  # Asumiendo que hay un campo 'asesor' en UniEconomicas
                unidad.save()
            
            return JsonResponse({'success': True})

        except Asesor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Asesor no encontrado'}, status=400)
        except UniEconomicas.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Unidad económica no encontrada'}, status=400)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


#Mostrar las unidades
@login_required
def consulta2(request):
    return render(request, 'consulta2.html')


#Continuar el seguimiento de una consulta
@login_required
def segConsulta(request):
    return render(request, 'seguimiento1.html')

#Dashboard
@login_required
def dash(request):
    return render(request, 'dash.html')


