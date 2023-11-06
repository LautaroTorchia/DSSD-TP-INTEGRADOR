from rest_framework import serializers
from .models import Coleccion, Mueble

class MuebleSerializer(serializers.ModelSerializer):
    plan_fabricacion = serializers.FileField(write_only=True)
    imagen = serializers.FileField(write_only=True)
    materiales = serializers.ListField(write_only=True)

    class Meta:
        model = Mueble
        fields = '__all__'

    def create(self, validated_data):
        plan_fabricacion = validated_data.pop('plan_fabricacion')
        imagen = validated_data.pop('imagen')
        materiales_data = validated_data.pop('materiales')
        validated_data['plan_fabricacion'] = plan_fabricacion
        validated_data['imagen'] = imagen
        
        instance = Mueble.objects.create(**validated_data)
        print(materiales_data)
        instance.materiales.set(materiales_data)  # Associate related materials using the set method
        return instance



class ColeccionSerializer(serializers.ModelSerializer):
    muebles = MuebleSerializer(many=True, read_only=True)

    class Meta:
        model = Coleccion
        fields = '__all__'
