# reservas/serializers.py

from rest_framework import serializers
from .models import ReservaMaterial, ReservaLugarFabricacion

class ReservaMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaMaterial
        fields = '__all__'


class ReservaLugarFabricacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaLugarFabricacion
        fields = '__all__'

