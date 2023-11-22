from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import RoleSerializer, UserRoleSerializer, UploadSerializer, UserRoleUploadSerializer, ViewDescriptorSerializer, ViewDescriptorUploadSerializer, PermissionRoleSerializer, PermissionRoleUploadSerializer, DRFTrackSerializer
from .models import Role, UserRole, ViewDescriptor, PermissionRole
from rest_framework_tracking.models import APIRequestLog
from authentication.models import User
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from tablib import Dataset
from .resources import RoleResource
from general_permissions.permissions import IsPermittedRBAC
from .utils.handler import get_historical_role_log, get_historical_permission_role_log, get_historical_user_role_log, get_historical_view_descriptor_log, get_historical_role_log_by_id, get_historical_permission_role_log_by_id, get_historical_user_role_log_by_id, get_historical_view_descriptor_log_by_id, get_user_role_by_date, get_permission_role_by_date, get_permission_user_by_date


class RoleListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):        
        return serializer.save()

    def get_queryset(self):        
        return self.queryset.all()

class RoleDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Role.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class RoleListView(ListAPIView):
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Role.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class UploadViewSet(LoggingMixin, ViewSet):
    serializer_class = UploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        Role_resource = RoleResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = Role_resource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    Role_resource.import_data(dataset, dry_run=False)
                    return Response({'message': 'The data has been loaded correctly.'}, status=status.HTTP_200_OK)
                else:
                    error_detail = "Charging error. Details:\n\n"
                    for n in result.rows:
                        for e in n.__dict__['errors']:
                            error_detail += str(e.__dict__['error']) + "\n"
                    return Response({'error': error_detail}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'File error. Please select an XLSX file.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class RoleAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def post(self, request):
        try:
            data = request.data
            user = request.user
            data["owner"] = user.id
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

class UserRoleListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.all()

class UserRoleDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserRoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = UserRole.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class UserRoleListView(ListAPIView):
    serializer_class = UserRoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = UserRole.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class UserRoleUploadViewSet(LoggingMixin, ViewSet):
    serializer_class = UserRoleUploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        UserRole_resource = UserRoleResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = UserRole_resource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    UserRole_resource.import_data(dataset, dry_run=False)
                    return Response({'message': 'The data has been loaded correctly.'}, status=status.HTTP_200_OK)
                else:
                    error_detail = "Charging error. Details:\n\n"
                    for n in result.rows:
                        for e in n.__dict__['errors']:
                            error_detail += str(e.__dict__['error']) + "\n"
                    return Response({'error': error_detail}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'File error. Please select an XLSX file.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class UserRoleAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = UserRoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def post(self, request):
        try:
            data = request.data
            user = request.user
            data["creator"] = user.id
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

class ViewDescriptorListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = ViewDescriptorSerializer
    queryset = ViewDescriptor.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.all()

class ViewDescriptorDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ViewDescriptorSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = ViewDescriptor.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class ViewDescriptorListView(ListAPIView):
    serializer_class = ViewDescriptorSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = ViewDescriptor.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class ViewDescriptorUploadViewSet(LoggingMixin, ViewSet):
    serializer_class = ViewDescriptorUploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        ViewDescriptor_resource = ViewDescriptorResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = ViewDescriptor_resource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    ViewDescriptor_resource.import_data(dataset, dry_run=False)
                    return Response({'message': 'The data has been loaded correctly.'}, status=status.HTTP_200_OK)
                else:
                    error_detail = "Charging error. Details:\n\n"
                    for n in result.rows:
                        for e in n.__dict__['errors']:
                            error_detail += str(e.__dict__['error']) + "\n"
                    return Response({'error': error_detail}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'File error. Please select an XLSX file.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class ViewDescriptorAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = ViewDescriptorSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def post(self, request):
        try:
            data = request.data
            user = request.user
            data["owner"] = user.id
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

class PermissionRoleListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = PermissionRoleSerializer
    queryset = PermissionRole.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.all()

class PermissionRoleDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = PermissionRoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = PermissionRole.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class PermissionRoleListView(ListAPIView):
    serializer_class = PermissionRoleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PermissionRole.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class PermissionRoleUploadViewSet(LoggingMixin, ViewSet):
    serializer_class = PermissionRoleUploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        PermissionRole_resource = PermissionRoleResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = PermissionRole_resource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    PermissionRole_resource.import_data(dataset, dry_run=False)
                    return Response({'message': 'The data has been loaded correctly.'}, status=status.HTTP_200_OK)
                else:
                    error_detail = "Charging error. Details:\n\n"
                    for n in result.rows:
                        for e in n.__dict__['errors']:
                            error_detail += str(e.__dict__['error']) + "\n"
                    return Response({'error': error_detail}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'File error. Please select an XLSX file.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


class PermissionRoleAPIView(LoggingMixin, generics.GenericAPIView):
    serializer_class = PermissionRoleSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def post(self, request):
        try:
            data = request.data
            user = request.user
            data["owner"] = user.id
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)