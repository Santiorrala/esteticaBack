from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(est_s_roles)
admin.site.register(est_s_funcion)
admin.site.register(est_s_funcion_rol)
admin.site.register(est_m_usuario)
admin.site.register(est_m_emplado)
admin.site.register(est_m_cliente)
admin.site.register(est_m_servicio)
admin.site.register(est_m_cita)
admin.site.register(est_m_cita_servicio)
admin.site.register(est_m_especialidad)