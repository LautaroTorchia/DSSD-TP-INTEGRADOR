from rest_framework import serializers
from .models import Actor, Material, ActorMaterial

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ActorMaterialSerializer(serializers.ModelSerializer):
    actor_nombre = serializers.CharField(source='actor.nombre', read_only=True)
    material_nombre = serializers.CharField(source='material.nombre', read_only=True)

    class Meta:
        model = ActorMaterial
        fields = ['id', 'actor', 'actor_nombre', 'material', 'material_nombre', 'cantidad_disponible', 'plazo_entrega_dias',"es_importado"]