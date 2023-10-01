from rest_framework import serializers
from .models import Role, UserRole, ViewDescriptor, PermissionRole
from rest_framework.serializers import Serializer, FileField
from rest_framework_tracking.models import APIRequestLog

class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Role
        fields = "__all__"

    def to_representation(self, instance):
        return ({
            "id": instance.id,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "owner": instance.owner.id,
            "owner_email": instance.owner.email,
            "denomination": instance.denomination,
            "description": instance.description,
            "is_archived": instance.is_archived
        })
        
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class UserRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRole
        fields = "__all__"

    def to_representation(self, instance):
        return ({
            "id": instance.id,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "creator": instance.creator.username,
            "username": instance.user_id.username,
            "user_id": instance.user_id.id,
            "role_denomination": instance.role_id.denomination,
            "role_id": instance.role_id.id
        })

        
class UserRoleUploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class ViewDescriptorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ViewDescriptor
        fields = "__all__"

    def to_representation(self, instance):
        return ({
            "id": instance.id,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "owner": instance.owner.id,
            "owner_email": instance.owner.email,
            "denomination": instance.denomination,
            "stack_name": instance.stack_name,
            "description": instance.description,
            "is_archived": instance.is_archived
        })
        
class ViewDescriptorUploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class PermissionRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PermissionRole
        fields = "__all__"

    def to_representation(self, instance):
        return ({
            "id": instance.id,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "owner": instance.owner.id,
            "owner_email": instance.owner.email,
            "view_id": instance.view_id.id,
            "view_id_denomination": instance.view_id.denomination,
            "role_id": instance.role_id,
            "role_id": instance.role_id.denomination
        })
        
class PermissionRoleUploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class DRFTrackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = APIRequestLog
        fields = "__all__"