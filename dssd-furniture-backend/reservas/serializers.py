# reservas/serializers.py

from rest_framework import serializers
from .models import ReservaMaterial, ReservaLugarFabricacion,MaterialEntregado

class ReservaMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaMaterial
        fields = '__all__'


class ReservaLugarFabricacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaLugarFabricacion
        fields = '__all__'


class MaterialEntregadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialEntregado
        fields = '__all__'
