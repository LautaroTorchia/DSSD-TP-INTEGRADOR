from rest_framework import serializers
from .models import Resource, ConfigResource, ConfigMessage
from rest_framework.serializers import Serializer, FileField

class ResourceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Resource
        fields = "__all__"
        
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class ConfigMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ConfigMessage
        fields = "__all__"

    def to_representation(self, instance):
        return ({
            "id": instance.id,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "name": instance.name,
            "description": instance.description,
            "keywords": instance.keywords,
            "content": instance.content,
            "is_archived": instance.is_archived
        })


class ConfigResourceSerializer(serializers.ModelSerializer):
	class Meta:
		model = ConfigResource
		fields = "__all__"
	def to_representation(self, instance):
		return ({
            "id": instance.id,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "name": instance.name,
            "description": instance.description,
            "resource_type": instance.resource_type,
            "keywords": instance.keywords,
            "language": instance.language,
            "content": instance.content.content            
        })
    
class ConfigResourceUploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']                        