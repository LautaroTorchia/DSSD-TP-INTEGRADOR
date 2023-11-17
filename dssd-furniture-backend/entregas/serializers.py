from rest_framework import serializers
from .models import OrdenDeEntrega,LotesFabricados,SedeDeDistribucion,VendedorFinal,AsociacionLoteOrdenEntrega

class OrdenDeEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeEntrega
        fields = '__all__'

class LotesFabricadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotesFabricados
        fields = '__all__'

class LugarDeDistribucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SedeDeDistribucion
        fields = '__all__'

class VendedorFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendedorFinal
        fields = '__all__'

class AsociacionLoteOrdenEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsociacionLoteOrdenEntrega
        fields = '__all__'