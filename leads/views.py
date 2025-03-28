from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate #Biblioteca de django que permite crear una coockie para la sesión del usuario
from django.db import IntegrityError
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

#----MAPAAA conversion de datos a json
def obtener_unidades_json(request):
    unidades = UniEconomicas.objects.values('Nombre_de_la_Unidad_Economica', 'Latitud', 'Longitud', 'estado')
    return JsonResponse(list(unidades), safe=False)
# ---- MAPA

#Detalle completo de las unidades
def detalle_unidad(request, unidad_id):
    try:
        unidad = UniEconomicas.objects.get(id=unidad_id)
        data = {
            "Nombre_de_la_Unidad_Economica": unidad.Nombre_de_la_Unidad_Economica,
            "Razon_social": unidad.Razon_social,
            "Nombre_de_clase_de_la_actividad": unidad.Nombre_de_clase_de_la_actividad,
            "Descripcion_estrato_personal_ocupado": unidad.Descripcion_estrato_personal_ocupado,
            "Nombre_de_la_vialidad": unidad.Nombre_de_la_vialidad,
            "Numero_exterior_o_kilometro": unidad.Numero_exterior_o_kilometro,
            "Letra_exterior": unidad.Letra_exterior,
            "Nombre_de_asentamiento_humano": unidad.Nombre_de_asentamiento_humano,
            "Codigo_postal": unidad.Codigo_postal,
            "Entidad_federetiva": unidad.Entidad_federetiva,
            "Municipio": unidad.Municipio,
            "Localidad": unidad.Localidad,
            "Numero_de_telefono": unidad.Numero_de_telefono,
            "Correo_electronico": unidad.Correo_electronico,
            "Sitio_en_Internet": unidad.Sitio_en_Internet,
        }
        return JsonResponse(data)
    except UniEconomicas.DoesNotExist:
        return JsonResponse({"error": "Unidad económica no encontrada"}, status=404)


#----- GENERAL-----
#Pantalla de home
def home(request):
    user_group = None
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Supervisor').exists():
            user_group = 'Supervisor'
        elif request.user.groups.filter(name='Asesor').exists():
            user_group = 'Asesor'

    return render(request, 'index.html', {'user_group': user_group})

#Inicio de sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'El nombre o la contraseña son incorrectos'
            })
        else:
            login(request, user)

            # Verificar si el usuario es Supervisor
            if user.groups.filter(name='Supervisor').exists():
                try:
                    supervisor = Supervisor.objects.get(user=user)
                    return redirect('accion')  # Supervisor redirigido a 'accion'
                except Supervisor.DoesNotExist:
                    return redirect('index')  # Si no se encuentra el supervisor, redirige a la página de inicio

            # Verificar si el usuario es Asesor
            elif user.groups.filter(name='Asesor').exists():
                try:
                    asesor = Asesor.objects.get(user=user)
                    return redirect('accionAses')  # Asesor redirigido a 'accionAses'
                except Asesor.DoesNotExist:
                    # Si el asesor no tiene un registro en la base de datos, se redirige a inicio
                    return render('index')

            else:
                return redirect('index')  # Si no es supervisor ni asesor, redirigir al inicio

#Salir de sesión
@login_required
def salir(request):
    logout(request)
    return redirect('index')


#------SUPERVISOR-----------

#Redirigir a la pantalla acción del supervisor
@login_required
def accion(request):
    return render(request, 'accion.html')

#Crear consultas a partir de estado, municipio y localidad
@login_required
def consulta1(request):
    return render(request, 'consulta1.html')

#Enlista las unidades econónicas
class UniEconomicaListView(ListView):
    model = UniEconomicas
    template_name = 'consulta2.html'
    context_object_name = 'unis'

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

#Filtrar los estados existentes
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
    # localidad = request.GET.get('localidad', '').strip()

    # Construcción dinámica del filtro
    filtros = {}
    if condicion:
        filtros['Nombre_de_clase_de_la_actividad__icontains'] = condicion
    if estado:
        filtros['Entidad_federetiva__icontains'] = estado
    if municipio:
        filtros['Municipio__icontains'] = municipio
    

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

#Vista a consulta2 (asignar asesores a unidades)
@login_required
def consulta2(request):
    return render(request, 'consulta2.html')

# Obtener unidades económicas asignadas a un asesor
def obtener_unidades_por_asesorSu(request):
    asesor_id = request.GET.get('asesor_id')

    if not asesor_id:
        return JsonResponse({'error': 'No se proporcionó un asesor'}, status=400)

    try:
        asesor = Asesor.objects.get(id=asesor_id)
        unidades = UniEconomicas.objects.filter(asesor=asesor).values(
            'Nombre_de_la_Unidad_Economica',
            'Entidad_federetiva',
            'Municipio',
            'Localidad',
            'Latitud',
            'Longitud',
            'FechaEdicion',
            'estado'
        )
        return JsonResponse({'unidades': list(unidades)})

    except Asesor.DoesNotExist:
        return JsonResponse({'error': 'Asesor no encontrado'}, status=404)

#Obtener los asesores
@login_required
def obtener_asesores(request):
    if request.method == 'GET':
        try:
            # Obtener el usuario logueado
            usuario = request.user
            # Verificar si el usuario es un supervisor
            supervisor = Supervisor.objects.get(user=usuario)
            # Filtrar los asesores que están bajo la supervisión de este usuario
            asesores = Asesor.objects.filter(supervisor=supervisor)
            # Convertir los asesores en un formato JSON
            asesor_data = [{'id': asesor.id, 'nombre': asesor.nomAses} for asesor in asesores]

            return JsonResponse({'asesores': asesor_data})

        except Supervisor.DoesNotExist:
            return JsonResponse({'error': 'El usuario no es un supervisor'}, status=403)

#Asignar unidades a asesor
def asignar_asesor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        asesor_id = data.get('asesor_id')
        unidades = data.get('unidades')

        try:
            asesor = Asesor.objects.get(id=asesor_id)
            for unidad_data in unidades:
                unidad = UniEconomicas.objects.get(Nombre_de_la_Unidad_Economica=unidad_data['Nombre'])
                # Aquí, asignamos el asesor a la unidad
                unidad.asesor = asesor
                unidad.save()

            return JsonResponse({'success': True})

        except Asesor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Asesor no encontrado'}, status=400)
        except UniEconomicas.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Unidad económica no encontrada'}, status=400)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

#Vista a verAsesor desde el Supervisor
@login_required
def verAsesor(request):
    return render(request, 'verAsesor.html')

#Guardar consulta en modal por editar
@csrf_exempt
def guardar_consulta(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del request
            nom_Cons = request.POST.get('nombreConsulta')
            fecha_Cons = request.POST.get('fechaConsulta')
            asesor_nombre = request.POST.get('asesor')  # Nombre del asesor recibido
            supervisor_nombre = request.POST.get('supervisor')  # Nombre del supervisor recibido
            uniEc = request.POST.get('unidades')  # Esto será un JSON con las unidades seleccionadas

            # Obtener la instancia del asesor desde la base de datos
            asesor = get_object_or_404(Asesor, nombre=asesor_nombre)  # Busca el asesor por nombre

            # Obtener la instancia del supervisor si es necesario
            supervisor = get_object_or_404(Supervisor, nombre=supervisor_nombre)  # Busca el supervisor por nombre

            # Si las unidades son un string JSON, conviértelo a un diccionario
            if uniEc:
                uniEc = json.loads(uniEc)  # Convierte el string JSON a un diccionario

            # Guardar la consulta en la base de datos
            consulta = Consulta(
                nom_Cons=nom_Cons,
                fecha_Cons=fecha_Cons,
                asesor=asesor,
                supervisor=supervisor,
                uniEc=uniEc  # Si el campo uniEc necesita ser un JSON, ya lo has procesado
            )
            consulta.save()

            return JsonResponse({'status': 'success', 'message': 'Consulta guardada con éxito.'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
# fin de edicion 

#Continuar el seguimiento de una consulta del supervisor
@login_required
def segConsulta(request):
    return render(request, 'seguimiento1.html')



#Dashboard del supervisor
@login_required
def dash(request):
    return render(request, 'dash.html')


# ----ASESOR--------

#Vista a acciones del asesor
def accionAses(request):
    return render(request, 'accionAses.html')

#Vista a seguimiento del asesor
@login_required
def asesorSeg(request):
    return render(request, 'asesorSeg.html')

def obtener_unidades_por_asesor(request):
    try:
        # Obtener el asesor basado en el usuario autenticado
        asesor = Asesor.objects.get(user=request.user)
        
        # Obtener las unidades económicas asignadas a ese asesor
        unidades = UniEconomicas.objects.filter(asesor=asesor).values(
            'id', 
            'Nombre_de_la_Unidad_Economica', 
            'Entidad_federetiva',
            'Municipio', 
            'Localidad', 
            'Latitud', 
            'Longitud',
            'FechaEdicion',
            'estado'
        )

        return JsonResponse({'unidades': list(unidades)})

    except Asesor.DoesNotExist:
        return JsonResponse({'error': 'Asesor no encontrado'}, status=404)
    
@csrf_exempt
def actualizar_estado_unidad(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            unidad_id = data.get("id")
            nuevo_estado = data.get("nuevo_estado")
            fecha_cambio = data.get("fecha_cambio")

            unidad = UniEconomicas.objects.get(id=unidad_id)
            unidad.estado = nuevo_estado
            unidad.FechaEdicion = fecha_cambio  # Asegúrate de tener este campo en el modelo
            unidad.save()

            return JsonResponse({"success": True})
        except UniEconomicas.DoesNotExist:
            return JsonResponse({"success": False, "error": "Unidad no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False}, status=400)