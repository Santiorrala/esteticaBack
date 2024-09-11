from django.db import models

# Create your models here.
class est_s_roles(models.Model):
    ro_codigo = models.PositiveBigIntegerField(primary_key=True)
    ro_nombre = models.CharField(max_length=100, default="", null=False)
    ro_descripcion = models.CharField(max_length=100, default="", null=True)
    ro_estado = models.BooleanField(default=True, null=False)

class est_s_funcion(models.Model):
    fu_codigo = models.PositiveBigIntegerField(primary_key=True)
    fu_descripcion = models.CharField(max_length=100, default="", null=False)
    fu_estado = models.BooleanField(default=True, null=False)

class est_s_funcion_rol(models.Model):
    fr_codigo = models.PositiveBigIntegerField(primary_key=True)
    fu_codigo = models.ForeignKey(est_s_funcion, on_delete=models.CASCADE)
    ro_codigo = models.ForeignKey(est_s_roles, on_delete=models.CASCADE)

class est_m_usuario(models.Model):
    us_codigo = models.PositiveBigIntegerField(primary_key=True)
    us_cedula = models.CharField(max_length=10, unique=True, null=False)
    us_nombre = models.CharField(max_length=100, default="", null=False)
    us_apellido = models.CharField(max_length=100, default="", null=False)
    us_correo = models.CharField(max_length=100, default="", null=False)
    us_telefono = models.CharField(max_length=10, default="", null=False)
    us_clave = models.CharField(max_length=100, null=False)
    ro_codigo = models.ForeignKey(est_s_roles, on_delete=models.CASCADE)
    us_estado = models.BooleanField(default=True, null=False)
    us_comentarios = models.CharField(max_length=100, default="", null=True)

class est_m_emplado(models.Model):
    em_codigo = models.PositiveBigIntegerField(primary_key=True)
    us_codigo = models.ForeignKey(est_m_usuario, on_delete=models.CASCADE)
    em_especialidad = models.CharField(max_length=100, default="", null=False)
    em_fecha_contrato = models.DateField(null=True)
    em_hora_entrada = models.CharField(max_length=100, null=False)
    em_hora_salida = models.CharField(max_length=100, null=False)
    em_imagen = models.CharField(max_length=100, default="", null=False)

class est_m_especialidad(models.Model):
    es_codigo = models.PositiveBigIntegerField(primary_key=True)
    es_nombre = models.CharField(max_length=100, default="", null=False)

class est_m_empleado_especialidad(models.Model):
    ee_codigo = models.PositiveBigIntegerField(primary_key=True)
    es_codigo = models.ForeignKey(est_m_especialidad, on_delete=models.CASCADE)
    em_codigo = models.ForeignKey(est_m_emplado, on_delete=models.CASCADE)

class est_m_cliente(models.Model):
    cl_codigo = models.PositiveBigIntegerField(primary_key=True)
    us_codigo = models.ForeignKey(est_m_usuario, on_delete=models.CASCADE)
    cl_forma_pago = models.CharField(max_length=100, null=True)
    cl_calificacion = models.PositiveBigIntegerField(null=False)

class est_m_categoria(models.Model):
    ca_codigo = models.PositiveBigIntegerField(primary_key=True)
    ca_nombre = models.CharField(max_length=100, null=True)
    es_codigo = models.ForeignKey(est_m_especialidad, on_delete=models.CASCADE)
    ca_imagen = models.CharField(max_length=100, null=True)

class est_m_servicio(models.Model):
    se_codigo = models.PositiveBigIntegerField(primary_key=True)
    se_nombre = models.CharField(max_length=100, null=False)
    se_descripcion = models.CharField(max_length=100, null=True)
    se_duracion = models.PositiveBigIntegerField(null=False)
    se_precio = models.CharField(max_length=100, null=False)
    ca_codigo = models.ForeignKey(est_m_categoria, on_delete=models.CASCADE)
    se_estado = models.BooleanField(default=True, null=False)
    
class est_m_cita(models.Model):
    ci_codigo = models.PositiveBigIntegerField(primary_key=True)
    ci_fecha = models.DateField(null=False)
    ci_hora = models.CharField(max_length=5, null=False)
    ci_estado = models.BooleanField(default=True, null=False)
    ci_nota = models.CharField(max_length=100, null=True)

class est_m_cita_servicio(models.Model):
    cs_codigo = models.PositiveBigIntegerField(primary_key=True)
    em_codigo = models.ForeignKey(est_m_emplado, on_delete=models.CASCADE)
    cl_codigo = models.ForeignKey(est_m_cliente, on_delete=models.CASCADE)
    ci_codigo = models.ForeignKey(est_m_cita, on_delete=models.CASCADE)
    se_codigo = models.ForeignKey(est_m_servicio, on_delete=models.CASCADE)

class est_m_correos(models.Model):
    co_codigo = models.PositiveBigIntegerField(primary_key=True)
    co_correo = models.CharField(max_length=9999, null=True)
    cs_email = models.CharField(max_length=100, null=True)
    cs_fecha = models.CharField(max_length=10, null=True)
    cs_hora = models.CharField(max_length=5, null=True)

class est_m_deshabilitados(models.Model):
    de_codigo = models.PositiveBigIntegerField(primary_key=True)
    de_fecha = models.CharField(max_length=10, null=True)
