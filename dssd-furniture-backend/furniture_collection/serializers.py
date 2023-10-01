from rest_framework import serializers
from .models import Coleccion, Mueble

class MuebleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mueble
        fields = '__all__'

class ColeccionSerializer(serializers.ModelSerializer):
    muebles = MuebleSerializer(many=True, read_only=True)

    class Meta:
        model = Coleccion
        fields = '__all__'
