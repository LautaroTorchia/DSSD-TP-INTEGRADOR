# reservas/serializers.py

from rest_framework import serializers
from .models import ReservaMaterial, ReservaLugarFabricacion

class ReservaMaterialSerializer(serializers.ModelSerializer):
    material_actor_name = serializers.ReadOnlyField(source='material.actor.nombre')
    material_name = serializers.ReadOnlyField(source='material.material.nombre')
    material_quantity = serializers.ReadOnlyField(source='material.cantidad_disponible')

    class Meta:
        model = ReservaMaterial
        fields = ['id', 'material', 'material_actor_name', 'material_name', 'material_quantity', 'fecha_entrega_pactada']


class ReservaLugarFabricacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaLugarFabricacion
        fields = '__all__'
