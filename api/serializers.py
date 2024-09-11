from rest_framework import serializers
from .models import *

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = est_m_categoria
        fields = ('ca_codigo', 'ca_nombre', 'es_codigo', 'ca_imagen')