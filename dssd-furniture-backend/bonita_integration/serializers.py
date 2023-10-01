# bonita_integration/serializers.py

from rest_framework import serializers
from .models import BonitaAPICall

class BonitaAPICallSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonitaAPICall
        fields = '__all__'
