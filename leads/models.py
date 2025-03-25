from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


#choices Status de Usuarios
tipos = [
    ('1','Cliente'),
    ('2','Prospecto'),
    ('3','No prospecto'),
    ('4','Cuenta ganada'),
    ('5','Descartado')
]


class Estado(models.Model):
    ESTADOS = [
    ('AGS', 'Aguascalientes'),
    ('BC', 'Baja California'),
    ('BCS', 'Baja California Sur'),
    ('CAM', 'Campeche'),
    ('COAH', 'Coahuila'),
    ('COL', 'Colima'),
    ('CHP', 'Chiapas'),
    ('CHIH', 'Chihuahua'),
    ('CDMX', 'Ciudad de México'),
    ('DGO', 'Durango'),
    ('GTO', 'Guanajuato'),
    ('GRO', 'Guerrero'),
    ('HGO', 'Hidalgo'),
    ('JAL', 'Jalisco'),
    ('MEX', 'México'),
    ('MICH', 'Michoacán'),
    ('MOR', 'Morelos'),
    ('NAY', 'Nayarit'),
    ('NL', 'Nuevo León'),
    ('OAX', 'Oaxaca'),
    ('PUE', 'Puebla'),
    ('QRO', 'Querétaro'),
    ('QROO', 'Quintana Roo'),
    ('SLP', 'San Luis Potosí'),
    ('SIN', 'Sinaloa'),
    ('SON', 'Sonora'),
    ('TAB', 'Tabasco'),
    ('TAMPS', 'Tamaulipas'),
    ('TLAX', 'Tlaxcala'),
    ('VER', 'Veracruz'),
    ('YUC', 'Yucatán'),
    ('ZAC', 'Zacatecas')
]

#Tabla Empresa
class Empresa(models.Model):
    nombreEmp = models.CharField(max_length=200, verbose_name='Empresa')
    giro = models.CharField(max_length=200, verbose_name='Giro')
    direccionEmp = models.CharField(max_length=250, verbose_name='Dirección de la empresa')

    def __str__(self):
        return '%s, %s, %s' % (self.nombreEmp, self.giro, self.direccionEmp)
    

#Table  Sucursal
class Sucursal(models.Model):
    nombreSuc = models.CharField(max_length=200, verbose_name='Sucursal')
    direccionSuc = models.CharField(max_length=250, verbose_name='Dirección de la sucursal')
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa')

    def __str__(self):
        return '%s, %s, %s' %(self.nombreSuc, self.direccionSuc, self.empresa)


#Table Supervisor
class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor', verbose_name='Usuario', null=True)
    nomSuper= models.CharField(max_length=250, verbose_name='Supervisor')
    sucursal= models.ForeignKey('Sucursal', on_delete=models.CASCADE, verbose_name='Sucursal')

    def __str__(self):
        return '%s' %(self.nomSuper)

#Table Asesor
class Asesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='asesor', verbose_name='Usuario', null=True)
    nomAses= models.CharField(max_length=250, verbose_name="Asesor")
    rutaAses=models.CharField(max_length=250, verbose_name='Ruta')
    supervisor=models.ForeignKey('Supervisor', on_delete=models.CASCADE, verbose_name='Supervisor')

    def __str__(self):
        return '%s, %s' %(self.nomAses, self.rutaAses)

#Table Unidades Economicas
class UniEconomicas(models.Model):
    ESTADO_CHOICES = [
        ('En atención', 'En atención'),
        ('Prospecto', 'Prospecto'),
        ('Cliente Nuevo', 'Cliente Nuevo'),
        ('Ya era Cliente', 'Ya era Cliente'),
        ('Descartado', 'Descartado'),
    ]

    id_Uni=models.CharField(max_length=200, verbose_name="ID Unidades economicas", null=True)
    CleeUni=models.CharField(max_length=100, verbose_name="Clee", null=True)
    Nombre_de_la_Unidad_Economica=models.CharField(max_length=250, verbose_name="Nombre de la unidad Economica", null=True)
    Razon_social=models.CharField(max_length=250, verbose_name="Razón social", null=True)
    Nombre_de_clase_de_la_actividad=models.CharField(max_length=250, verbose_name="Nombre de la clase de la actividad", null=True)
    Descripcion_estrato_personal_ocupado=models.CharField(max_length=300, verbose_name="Descripcion del estrato", null=True)
    Nombre_de_la_vialidad=models.CharField(max_length=250,verbose_name="Nombre de la vialidad", null=True)
    Numero_exterior_o_kilometro=models.CharField(max_length=20, verbose_name="Numero exterior", null=True)
    Letra_exterior=models.CharField(max_length=200, verbose_name="Letra exterior", null=True)
    Nombre_de_asentamiento_humano=models.CharField(max_length=250, verbose_name="Asentamiento humano", null=True)
    Codigo_postal=models.CharField(max_length=6, verbose_name="Codigo postal", null=True)
    Entidad_federetiva=models.CharField(max_length=250, verbose_name="Estado", null=True)
    Municipio=models.CharField(max_length=250, verbose_name="Municipio", null=True)
    Localidad=models.CharField(max_length=250, verbose_name="Localidad", null=True)
    Numero_de_telefono=models.CharField(max_length=13, verbose_name="Telefono", null=True)
    Correo_electronico=models.CharField(max_length=250, verbose_name="Correo", null=True)
    Sitio_en_Internet=models.CharField(max_length=250,verbose_name="Sitio web", null=True)
    Latitud=models.CharField(max_length=200, verbose_name="Latitud", null=True)
    Longitud=models.CharField(max_length=200, verbose_name="Longitud", null=True)
    Fecha_de_incorporacion_al_denue=models.CharField(max_length=20, verbose_name="Fecha de incorporación al denue", null=True)
    asesor = models.ForeignKey(Asesor, on_delete=models.CASCADE, verbose_name="Asesor", null=True, blank=True, related_name="unidades")
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='En atención')
    FechaEdicion = models.DateField(null=True, blank=True)



    
#Tabla Consultas
class Consulta(models.Model):
    nom_Cons=models.CharField(max_length=200, verbose_name='Consulta')
    fecha_Cons= models.DateField(verbose_name='Fecha', null= False)
    asesor=models.ForeignKey('Asesor', on_delete=models.CASCADE, verbose_name='Asesor')
    uniEc=models.ForeignKey('UniEconomicas', on_delete=models.CASCADE, verbose_name='Unidades Economicas')
