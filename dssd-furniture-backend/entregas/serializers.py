from rest_framework import serializers
from .models import OrdenDeEntrega

class OrdenDeEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeEntrega
        fields = '__all__'
