from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ResourceSerializer, ConfigResourceSerializer, UploadSerializer, ConfigResourceUploadSerializer, ConfigMessageSerializer
from .models import Resource, ConfigResource, ConfigMessage
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from tablib import Dataset
from .resources import Resource
from general_permissions.permissions import IsPermittedRBAC
from .utils.handler import getActionToDeploy


class ResourceListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):
        return serializer.save()
    def get_queryset(self):
        return self.queryset

class ResourceDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ResourceSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Resource.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class ResourceListView(ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Resource.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class UploadViewSet(LoggingMixin, ViewSet):
    serializer_class = UploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        Resource_resource = ResourceResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = Resource_resource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    Resource_resource.import_data(dataset, dry_run=False)
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

########
#ConfigResource
########

class ConfigResourceListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = ConfigResourceSerializer
    queryset = ConfigResource.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):
        return serializer.save()
    def get_queryset(self):
        return self.queryset

class ConfigResourceDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ConfigResourceSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = ConfigResource.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class ConfigResourceListView(ListAPIView):
    serializer_class = ConfigResourceSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = ConfigResource.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)

class ConfigResourceUploadViewSet(LoggingMixin, ViewSet):
    serializer_class = ConfigResourceUploadSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def list(self, request):
        return Response("GET API")
    def create(self, request):        
        ConfigResource_ConfigResource = ConfigResourceConfigResource()
        dataset = Dataset()
        try:
            file_uploaded = request.FILES.get('file_uploaded')
            content_type = file_uploaded.content_type
            if file_uploaded._name.endswith('.xlsx'):            
                imported_data = dataset.load(file_uploaded.read())        
                result = ConfigResource_ConfigResource.import_data(dataset, dry_run=True)        
                if not result.has_errors():            
                    ConfigResource_ConfigResource.import_data(dataset, dry_run=False)
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

class ConfigResourceCheckView(LoggingMixin, generics.GenericAPIView):
    serializer_class = ConfigResourceSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC, )
    
    def post(self, request):
        try:
            data = request.data            
            action = getActionToDeploy()
            message = {"Action": action}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as ex:
            from progralog.utils import generic_progra_log_error
            message = generic_progra_log_error()
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

########
#ConfigMessage
########

class ConfigMessageListAPIView(LoggingMixin, ListCreateAPIView):
    serializer_class = ConfigMessageSerializer
    queryset = ConfigMessage.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)

    def perform_create(self, serializer):
        return serializer.save()
    def get_queryset(self):
        return self.queryset

class ConfigMessageDetailAPIView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ConfigMessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = ConfigMessage.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class ConfigMessageListView(ListAPIView):
    serializer_class = ConfigMessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = ConfigMessage.objects.all()
    filter_backends = (DynamicSearchFilter, OrderingFilter)
