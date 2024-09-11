from django.shortcuts import render
from .serializers import CategoriaSerializer
from rest_framework import generics
from .models import *

# Create your views here.

class CategoriaAddView(generics.CreateAPIView):
    queryset = est_m_categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaView(generics.ListAPIView):
    queryset = est_m_categoria.objects.all()
    serializer_class = CategoriaSerializer

from django.db import connection
from django.http import JsonResponse
cursor = connection.cursor()
#obtener todas las categorias
def pa_gCategorias(req):
    busca_correo() #enviar recordatorios pendientes
    with connection.cursor() as cursor:
        cursor.execute('call pa_gCategorias()')
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'ca_codigo': row[0],
            'ca_nombre': row[1],
            'es_codigo': row[2],
            'ca_imagen': row[3],
        })

    return JsonResponse(categorias, safe=False)

#obtener las categorias por codigo y/o nombre
def pa_cCategorias(request):
    # Obtén los parámetros desde la URL
    ca_codigo = request.GET.get('ca_codigo', -1)
    ca_nombre = request.GET.get('ca_nombre', '')

    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        # Ejecuta el procedimiento almacenado con los parámetros
        cursor.execute('call pa_cCategorias(%s, %s)', [ca_codigo, ca_nombre])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'ca_codigo': row[0],
            'ca_nombre': row[1],
            'es_codigo': row[2],
            'ca_imagen': row[3],
        })

    return JsonResponse(categorias, safe=False)


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

#loguearse
@csrf_exempt
@require_POST
def login(request):
    # Obtén los parámetros desde la URL
    data = json.loads(request.body.decode('utf-8'))
    us_cedula = data.get('us_cedula')
    us_clave = data.get('us_clave')

    busca_correo() #enviar recordatorios pendientes

    if not us_cedula or not us_clave:
            return JsonResponse({
                'codigo_error': 3,
                'mensaje': 'Parámetros faltantes'
            }, status=400)

    with connection.cursor() as cursor:
        # Ejecuta el procedimiento almacenado con los parámetros
        cursor.execute('call pa_login(%s, %s)', [us_cedula, us_clave])
        result = cursor.fetchall()

    if result:
        row = result[0]
        codigo_error = row[0]

        if codigo_error == -1:
            # Si el código de error es -1, devolver un JSON con el código de error y el mensaje
            return JsonResponse({
                'codigo_error': 1,
                'mensaje': 'Usuario no encontrado'
            })

        else:
            return JsonResponse({
                'us_codigo': row[0],
                'us_cedula': row[1],
                'us_nombre': row[2],
                'us_apellido': row[3],
                'us_correo': row[4],
                'us_telefono': row[5],
                'ro_codigo': row[6]
            })

    # En caso de que no haya resultados, también manejar el caso de error
    return JsonResponse({
        'codigo_error': 2,
        'mensaje': 'Clave incorrecta'
    })

#obtener los servicios por codigo de servicioy/o codigo de categoria
def pa_cServicios(request):
    # Obtén los parámetros desde la URL
    se_codigo = request.GET.get('se_codigo', -1)
    ca_codigo = request.GET.get('ca_codigo', 0)

    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        cursor.execute('call pa_cServicios(%s, %s)', [se_codigo, ca_codigo])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'se_codigo': row[0],
            'se_nombre': row[1],
            'se_descripcion': row[2],
            'se_duracion': row[3],
            'se_precio': row[4],
            'ca_codigo_id': row[5],
        })

    return JsonResponse(categorias, safe=False)

#obtener los empleados que pueden dar ese servicio
def pa_cEmpleadosXServicio(request):
    # Obtén los parámetros desde la URL
    se_codigo = request.GET.get('se_codigo', 0)

    #busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        cursor.execute('call pa_cEmpleadoxServicio(%s)', [se_codigo])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'em_nombre': row[0],
            'em_codigo': row[1],
            'us_codigo': row[2],
            'em_especialidad': row[3],
            'em_hora_entrada': row[4],
            'em_hora_salida': row[5],
            'em_imagen': row[6],
        })

    return JsonResponse(categorias, safe=False)

#obtener los horarios disponibles segun una fecha 
def pa_horariosXFecha(request):
    # Obtén los parámetros desde la URL
    e_fecha = request.GET.get('e_fecha'),
    e_empleado = request.GET.get('e_empleado'),

    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        cursor.execute('call pa_horariosXFecha(%s,%s)', [e_fecha, e_empleado])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'hora': row[0],
            'ci_hora': row[1],
            'em_codigo': row[2]
        })

    return JsonResponse(categorias, safe=False)

import logging
logger = logging.getLogger(__name__)

#agendar la cita
@csrf_exempt
@require_POST
def pa_agendarCita(request):
    data = json.loads(request.body.decode('utf-8'))
    e_fecha = data.get('e_fecha')
    e_hora = data.get('e_hora')
    e_empleado = data.get('e_empleado')
    e_cliente = data.get('e_cliente')
    e_servicio = data.get('e_servicio')
    busca_correo() #enviar recordatorios pendientes

    if not e_fecha or not e_fecha or not e_hora or not e_empleado or not e_cliente or not e_servicio:
        return JsonResponse({
            'codigo_error': 88,
            'mensaje': 'Parámetros faltantes'
        }, status=400)

    with connection.cursor() as cursor:
        cursor.execute('call agendarCita(%s, %s, %s, %s, %s)', [e_fecha, e_hora, e_empleado, e_cliente, e_servicio])
        result = cursor.fetchall()

    if result:
        row = result[0]
        codigo_error = row[0]
        return JsonResponse({
            'codigo_error': row[0],
            'mensaje': row[1]
        })

    # En caso de que no haya resultados, también manejar el caso de error
    return JsonResponse({
        'codigo_error': 2,
        'mensaje': 'Agenda no guardada'
    })

from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

#enviar correo al agendar la cita
def enviar_correo(request):
    e_cita = request.GET.get('e_cita')
    mensaje = ''
    correo = ''
    busca_correo() #enviar recordatorios pendientes
    with connection.cursor() as cursor:
        cursor.execute('call pa_creaCorreo(%s)', [e_cita])
        result = cursor.fetchall()

    if result:
        row = result[0]
        mensaje = row[0]
        correo = row [1]

    subject = 'Estetica Antnella - AGENDA'
    message = mensaje
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['webadasdeanfibius@gmail.com']
    send_mail(subject, message, from_email, recipient_list)

    return JsonResponse({
        'codigo_error': 0,
        'mensaje': 'Correo Enviado ' + mensaje + " - " + correo
    })

#obtener el historial con respecto al tipo de usuario
def pa_getHistorial(request):
    # Obtén los parámetros desde la URL
    e_usuario = request.GET.get('e_usuario')
    e_tipo = request.GET.get('e_tipo')
    e_cliemp = request.GET.get('e_cliemp')
    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        # Ejecuta el procedimiento almacenado con los parámetros
        cursor.execute('call pa_getHistorial(%s, %s, %s)', [e_usuario, e_tipo, e_cliemp])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'codigo_cita': row[0],
            'hora_cita': row[1],
            'codigo_servicio': row[2],
            'codigo_nombre': row[3],
            'duracion': row[4],
            'codigo_estado': row[5],
            'estado': row[6],
            'cliente': row[7],
            'empleado': row[8],
            'ci_fecha': row[9],
            'fecha_hora': row[10]
        })

    return JsonResponse(categorias, safe=False)

#cancelar una cita
def pa_cancelarCita(request):
    e_cita = request.GET.get('e_cita')
    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        cursor.execute('call pa_cancelaCita(%s)', [e_cita])
        result = cursor.fetchall()

    return JsonResponse({
        'codigo_error': 0,
        'mensaje': 'Cita Cancelada'
    })

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import HexColor
from io import BytesIO

#crear pdf para el reporte
def generate_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, "Hello, this is a PDF generated with ReportLab!")
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

from reportlab.lib.units import inch
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
def prueba_pdf(request):
    e_categoria = request.GET.get('e_categoria')
    e_servicio = request.GET.get('e_servicio')
    e_fecha_inicio = request.GET.get('e_fecha_inicio')
    e_fecha_fin = request.GET.get('e_fecha_fin')

    with connection.cursor() as cursor:
        cursor.execute('call pa_generaPdfEsp(%s, %s, %s, %s)', [e_categoria, e_servicio, e_fecha_inicio, e_fecha_fin])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'ca_codigo': row[0],
            'ca_nombre': row[1],
            'se_codigo': row[2],
            'se_nombre': row[3],
            'ci_fecha': row[4],
            'ci_hora': row[5],
            'cliente': row[6],
            'empleado': row[7],
            'ci_estado': row[8],
            'estado_des': row[9]
        })
    
    if categorias:
        first_record = categorias[0]
        categoria_pdf = first_record["ca_nombre"]
        servicio_pdf = first_record["se_nombre"]

    table_data = [["Categoria", "Servicio", "Fecha", "Hora", "Ciente", "Empleado", "Estado"]]  # Encabezados
    for item in categorias:
        table_data.append([item["ca_nombre"], item["se_nombre"], item["ci_fecha"], item["ci_hora"], item["cliente"], item["empleado"], item["estado_des"]])

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    today = datetime.now().strftime('%d de %B de %Y')
    date_paragraph = Paragraph(f"Fecha: {today}", normal_style)
    elements.append(date_paragraph)

    title = Paragraph('HISTORIAL DE AGENDA', title_style)
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", normal_style))

    categoria_Par = Paragraph('Categoria:  ' + categoria_pdf, title_style)
    elements.append(categoria_Par)
    servicio_Par = Paragraph('Servicio:  ' + servicio_pdf, title_style)
    elements.append(servicio_Par)
    elements.append(Paragraph("<br/>", normal_style))

    table = Table(table_data, colWidths=[1*inch, 2*inch, 1*inch, 1*inch, 2*inch, 2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#CCCCCC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#000000')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#000000')),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    with open('generated_report.pdf', 'wb') as f:
        f.write(buffer.getvalue())
        
    return HttpResponse(buffer, content_type='application/pdf')

def prueba_pdf1(request):
    e_fecha_inicio = request.GET.get('e_fecha_inicio')
    e_fecha_fin = request.GET.get('e_fecha_fin')

    with connection.cursor() as cursor:
        # Ejecuta el procedimiento almacenado con los parámetros
        cursor.execute('call pa_generaPdfTodo(%s, %s)', [e_fecha_inicio, e_fecha_fin])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'ca_codigo': row[0],
            'ca_nombre': row[1],
            'se_codigo': row[2],
            'se_nombre': row[3],
            'ci_fecha': row[4],
            'ci_hora': row[5],
            'cliente': row[6],
            'empleado': row[7],
            'ci_estado': row[8],
            'estado_des': row[9]
        })
    
    if categorias:
        first_record = categorias[0]
        categoria_pdf = first_record["ca_nombre"]
        servicio_pdf = first_record["se_nombre"]
        empleado_pdf = first_record["empleado"]
    else:
        header_name = "Desconocido"
        header_age = "Desconocido"
        header_city = "Desconocido"

    # Convertir los datos a un formato adecuado para ReportLab
    table_data = [["Categoria", "Servicio", "Fecha", "Hora", "Ciente", "Empleado", "Estado"]]  # Encabezados
    for item in categorias:
        table_data.append([item["ca_nombre"], item["se_nombre"], item["ci_fecha"], item["ci_hora"], item["cliente"], item["empleado"], item["estado_des"]])

    # Crear el buffer
    buffer = BytesIO()

    # Crear el PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Obtener estilos
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    # Agregar fecha
    today = datetime.now().strftime('%d de %B de %Y')
    date_paragraph = Paragraph(f"Fecha: {today}", normal_style)
    elements.append(date_paragraph)

    # Agregar título
    title = Paragraph('HISTORIAL DE AGENDA', title_style)
    elements.append(title)
    # Agregar un espacio antes de la tabla
    elements.append(Paragraph("<br/><br/>", normal_style))

    # Crear la tabla
    table = Table(table_data, colWidths=[1*inch, 2*inch, 1*inch, 1*inch, 2*inch, 2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#CCCCCC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#000000')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#000000')),
    ]))
    elements.append(table)

    # Construir el PDF
    doc.build(elements)
    buffer.seek(0)

    with open('generated_report.pdf', 'wb') as f:
        f.write(buffer.getvalue())

    return HttpResponse(buffer, content_type='application/pdf')

#crear reporte general
def cargar_todo(request):
    e_fecha_inicio = request.GET.get('e_fecha_inicio')
    e_fecha_fin = request.GET.get('e_fecha_fin')

    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        # Ejecuta el procedimiento almacenado con los parámetros
        cursor.execute('call pa_generaPdfTodo(%s, %s)', [e_fecha_inicio, e_fecha_fin])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'ca_codigo': row[0],
            'ca_nombre': row[1],
            'se_codigo': row[2],
            'se_nombre': row[3],
            'ci_fecha': row[4],
            'ci_hora': row[5],
            'cliente': row[6],
            'empleado': row[7],
            'ci_estado': row[8],
            'estado_des': row[9]
        })

    return JsonResponse(categorias, safe=False)

def cargar_esp(request):
    e_categoria = request.GET.get('e_categoria')
    e_servicio = request.GET.get('e_servicio')
    e_fecha_inicio = request.GET.get('e_fecha_inicio')
    e_fecha_fin = request.GET.get('e_fecha_fin')

    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        cursor.execute('call pa_generaPdfEsp(%s, %s, %s, %s)', [e_categoria, e_servicio, e_fecha_inicio, e_fecha_fin])
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'ca_codigo': row[0],
            'ca_nombre': row[1],
            'se_codigo': row[2],
            'se_nombre': row[3],
            'ci_fecha': row[4],
            'ci_hora': row[5],
            'cliente': row[6],
            'empleado': row[7],
            'ci_estado': row[8],
            'estado_des': row[9]
        })

    return JsonResponse(categorias, safe=False)

#reistrar un cliente
@csrf_exempt
@require_POST
def registrar(request):
    data = json.loads(request.body.decode('utf-8'))
    us_cedula = data.get('us_cedula')
    e_nombre = data.get('e_nombre')
    e_apellido = data.get('e_apellido')
    e_correo = data.get('e_correo')
    e_telefono = data.get('e_telefono')
    e_clave = data.get('e_clave')

    busca_correo() #enviar recordatorios pendientes

    if not us_cedula or not e_clave:
            return JsonResponse({
                'codigo_error': 3,
                'mensaje': 'Parámetros faltantes'
            }, status=400)

    with connection.cursor() as cursor:
        cursor.execute('call pa_registrarCliente(%s, %s, %s, %s, %s, %s)', [us_cedula, e_nombre, e_apellido, e_correo, e_telefono, e_clave])
        result = cursor.fetchall()

    if result:
        row = result[0]
        codigo_error = row[0]
        mensaje = row[1]

    return JsonResponse({
        'codigo_error': codigo_error,
        'mensaje': mensaje
    })

#actualizar datos de usuario
@csrf_exempt
@require_POST
def actualizar(request):
    data = json.loads(request.body.decode('utf-8'))
    e_codigo = data.get('e_codigo')
    e_correo = data.get('e_correo')
    e_telefono = data.get('e_telefono')
    e_clave = data.get('e_clave')
    e_clave1 = data.get('e_clave1')

    busca_correo() #enviar recordatorios pendientes

    if not e_codigo or not e_clave:
            return JsonResponse({
                'codigo_error': 3,
                'mensaje': 'Parámetros faltantes'
            }, status=400)

    with connection.cursor() as cursor:
        cursor.execute('call pa_actualizarCliente(%s, %s, %s, %s, %s)', [e_codigo, e_correo, e_telefono, e_clave, e_clave1])
        result = cursor.fetchall()

    if result:
        row = result[0]
        codigo_error = row[0]
        mensaje = row[1]

    return JsonResponse({
        'codigo_error': codigo_error,
        'mensaje': mensaje
    })

def busca_correo():
    with connection.cursor() as cursor:
        cursor.execute('call pa_buscaCorreo()')
        result = cursor.fetchall()
    
    mensaje = ''
    e_correo = ''

    if result:
        row = result[0]
        codigo = row[0]
        mensaje = row [1]
        e_correo = row [2]
        subject = 'Estetica Antonella - RECORDATORIO'
        #premensaje = '<!DOCTYPE html> <html lang="es"> <head>     <meta charset="UTF-8">     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <title>Confirmación de Cita</title>     <style>              .body {             margin: 0;             padding: 5px;             background-color: #000000;             color: #333;             display: flex;             justify-content: center;             align-items: center;             height: 100vh;         }         .justificado{             text-align: justify;         }         .container {             width: 70%;             max-width: 800px;             margin: auto;             padding: 30px;             background: #fff;             border-radius: 8px;             background-color: #f4f4f4;             box-shadow: 0 0 10px rgba(0,0,0,0.1);         }         .header img {             width: 100%;             height: auto;             max-height: 310px;             object-fit: cover;             border-radius: 1px 1px 0 0;         }         .content p {             color: #000000;             line-height: 20px;             font: Brush Script MT, sans-serif;         }         .content h2, h3 {             padding: 1px;             color: #000;             line-height: 20px;         }                .footer {             padding: 5px;             text-align: center;             font-size: 0.9em;             color: #000;         }     </style> </head> <body>     <div class="container" >         <div class="header">             <img src="LOGO.png" alt="logo de la estética">         </div>         <div class="content">         <p class="justificado">             <center>             <h3>Confirmación de cita en el centro de belleza</h3>             <h2>"Antonella"</h2>             <p>Hola,</p>             <p>¡Gracias por agendar con nosotros en "Antonella"!</p>             <p>Nos complace confirmarte que tu cita fue programada con éxito.</p>             <p>' + men_correo + '</p>             <p>Si tienes alguna duda, contactanos al</p>             <p><b>Cel: 093-951-3373 </b></p>             <p>¡Esperamos verte pronto y brindarte un excelente servicio!</p>             </center         </p>         </div>         <div class="footer">             <p>¡Que tengas un lindo día!</p>                     </div>     </div> </p> </body> </html>'
        message = mensaje
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [e_correo]
        send_mail(subject, message, from_email, recipient_list)

#correo de recuperacion de contraseña
@csrf_exempt
@require_POST
def enviar_correo_recuperado(request):
    data = json.loads(request.body.decode('utf-8'))
    e_usuario = data.get('e_usuario')
    e_correo = data.get('e_correo')
    codigo = ''
    mensaje = ''
    men_correo = ''

    with connection.cursor() as cursor:
        cursor.execute('call pa_recuperarCliente(%s, %s)', [e_usuario, e_correo])
        result = cursor.fetchall()

    if result:
        row = result[0]
        codigo = row[0]
        mensaje = row [1]
        men_correo = row [2]

    if codigo == 0 or codigo == '0':
        subject = 'Estetica Antonella - RECUPERAR'
        #premensaje = '<!DOCTYPE html> <html lang="es"> <head>     <meta charset="UTF-8">     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <title>Confirmación de Cita</title>     <style>              .body {             margin: 0;             padding: 5px;             background-color: #000000;             color: #333;             display: flex;             justify-content: center;             align-items: center;             height: 100vh;         }         .justificado{             text-align: justify;         }         .container {             width: 70%;             max-width: 800px;             margin: auto;             padding: 30px;             background: #fff;             border-radius: 8px;             background-color: #f4f4f4;             box-shadow: 0 0 10px rgba(0,0,0,0.1);         }         .header img {             width: 100%;             height: auto;             max-height: 310px;             object-fit: cover;             border-radius: 1px 1px 0 0;         }         .content p {             color: #000000;             line-height: 20px;             font: Brush Script MT, sans-serif;         }         .content h2, h3 {             padding: 1px;             color: #000;             line-height: 20px;         }                .footer {             padding: 5px;             text-align: center;             font-size: 0.9em;             color: #000;         }     </style> </head> <body>     <div class="container" >         <div class="header">             <img src="LOGO.png" alt="logo de la estética">         </div>         <div class="content">         <p class="justificado">             <center>             <h3>Confirmación de cita en el centro de belleza</h3>             <h2>"Antonella"</h2>             <p>Hola,</p>             <p>¡Gracias por agendar con nosotros en "Antonella"!</p>             <p>Nos complace confirmarte que tu cita fue programada con éxito.</p>             <p>' + men_correo + '</p>             <p>Si tienes alguna duda, contactanos al</p>             <p><b>Cel: 093-951-3373 </b></p>             <p>¡Esperamos verte pronto y brindarte un excelente servicio!</p>             </center         </p>         </div>         <div class="footer">             <p>¡Que tengas un lindo día!</p>                     </div>     </div> </p> </body> </html>'
        message = men_correo
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [e_correo]
        send_mail(subject, message, from_email, recipient_list)

    return JsonResponse({
        'codigo_error': codigo,
        'mensaje': mensaje
    })

#obtener los dias que no estan disponibles
def pa_gDias(req):

    busca_correo() #enviar recordatorios pendientes
    with connection.cursor() as cursor:
        cursor.execute('call pa_obtenerDias()')
        result = cursor.fetchall()

    categorias = []
    for row in result:
        categorias.append({
            'de_codigo': row[0],
            'de_fecha': row[1],
            'nombre': row[2]
        })

    return JsonResponse(categorias, safe=False)

#registrar un dia como no disponible
@csrf_exempt
@require_POST
def registrarDia(request):
    data = json.loads(request.body.decode('utf-8'))
    busca_correo() #enviar recordatorios pendientes
    
    if not isinstance(data, list):
        return JsonResponse({
            'codigo_error': 1,
            'mensaje': 'El cuerpo de la solicitud debe ser un array de objetos'
        }, status=400)
    
    errores = []
    exitos = []
    
    with connection.cursor() as cursor:
        cursor.execute('call pa_limpiarDias()')
        result = cursor.fetchall()
    
    if result:
        for item in data:
            de_codigo = item.get('de_codigo')
            de_fecha = item.get('de_fecha')

            if de_fecha == "":
                errores.append({
                    'codigo_error': 3,
                    'mensaje': 'Parámetros faltantes',
                    'item': item
                })
                continue

            with connection.cursor() as cursor:
                cursor.callproc('pa_registrarDias', [de_fecha])
                result = cursor.fetchall()
            
            if result:
                row = result[0]
                codigo_error = row[0]
                
                if codigo_error != 0:  # Asumiendo 0 indica éxito
                    errores.append({
                        'codigo_error': codigo_error,
                        'mensaje': mensaje,
                        'item': item
                    })
                else:
                    exitos.append(item)
        
        if errores:
            return JsonResponse({
                'codigo_error': 4,
                'mensaje': 'Algunos registros no se procesaron',
                'errores': errores,
                'exitos': exitos
            }, status=400)

    
    
    return JsonResponse({
        'codigo_error': 0,
        'mensaje': 'Todos los registros se procesaron exitosamente',
        'exitos': exitos
    })

#confirmar cita y cambiarle el estado
def pa_confirmarCita(request):
    e_cita = request.GET.get('e_cita')
    busca_correo() #enviar recordatorios pendientes

    with connection.cursor() as cursor:
        cursor.execute('call pa_cambioEstadoCita(%s)', [e_cita])
        result = cursor.fetchall()

    return JsonResponse({
        'codigo_error': 0,
        'mensaje': 'Cita Confirmada'
    })