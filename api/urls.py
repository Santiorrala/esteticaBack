from django.urls import path, include
from .views import *

urlpatterns = [
    #path('', main),
    path('categoriaadd', CategoriaAddView.as_view()),
    path('categoria', CategoriaView.as_view()),
    path('gcategoria', pa_gCategorias),
    path('ccategoria/', pa_cCategorias, name='ccategoria'),
    path('login/', login, name='login'),
    path('cservicio/', pa_cServicios, name='cservicio'),
    path('cempleadoxservicio/', pa_cEmpleadosXServicio, name='cempleadoxservicio'),
    path('pa_horariosXFecha/', pa_horariosXFecha, name='pa_horariosXFecha'),
    path('agendarCita/', pa_agendarCita, name='agendarCita'),
    path('enviocorreo/', enviar_correo, name='enviocorreo'),
    path('gethistorial/', pa_getHistorial, name='gethistorial'),
    path('getcancelar/', pa_cancelarCita, name='getcancelar'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('prueba_pdf/', prueba_pdf, name='prueba_pdf'),
    path('prueba_pdf1/', prueba_pdf1, name='prueba_pdf1'),
    path('cargartodo/', cargar_todo, name='cargartodo'),
    path('cargaresp/', cargar_esp, name='cargaresp'),
    path('registrar/', registrar, name='registrar'),
    path('actualizar/', actualizar, name='actualizar'),
    path('recuperar/', enviar_correo_recuperado, name='recuperar'),
    path('gdias', pa_gDias, name='gdias'),
    path('idias/', registrarDia, name='idias'),
    path('getconfirmar/', pa_confirmarCita, name='getconfirmar'),
]
