from .models import Coleccion, Mueble
from .serializers import ColeccionSerializer, MuebleSerializer
from general_permissions.permissions import IsPermittedRBAC
from rest_framework import generics,permissions
from rest_framework import status
from rest_framework.response import Response
from .utils import upload_file_to_drive, get_image_from_drive

class ColeccionListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Coleccion.objects.all()
    serializer_class = ColeccionSerializer

class ColeccionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Coleccion.objects.all()
    serializer_class = ColeccionSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Mueble
from .serializers import MuebleSerializer

class MuebleListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC)
    queryset = Mueble.objects.all()
    serializer_class = MuebleSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_fabricacion = request.data.get('plan_fabricacion')
        imagen = request.data.get('imagen')
        materiales_data = request.data.getlist('materiales')  # Get materiales data as a list
        
        plan_fabricacion_file_id = upload_file_to_drive(plan_fabricacion.read(), plan_fabricacion.name)
        imagen_file_id = upload_file_to_drive(imagen.read(), imagen.name)

        if plan_fabricacion_file_id and imagen_file_id:
            validated_data = serializer.validated_data
            validated_data['plan_fabricacion'] = plan_fabricacion_file_id
            validated_data['imagen'] = imagen_file_id
            validated_data['materiales'] = materiales_data  # Pass materiales list to serializer

            instance = serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'File upload failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class MuebleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Mueble.objects.all()
    serializer_class = MuebleSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        imagen_id = instance.imagen  # Assuming imagen is the ID of the image on Google Drive
        plan_fabricacion_id = instance.plan_fabricacion  # Assuming plan_fabricacion is the ID of the plan on Google Drive

        # Fetch image content from Google Drive
        imagen_content = get_image_from_drive(imagen_id)
        plan_fabricacion_content = get_image_from_drive(plan_fabricacion_id)

        # Get the serializer data
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Add image content to the response data
        data['imagen_content'] = imagen_content
        data['plan_fabricacion_content'] = plan_fabricacion_content

        return Response(data)