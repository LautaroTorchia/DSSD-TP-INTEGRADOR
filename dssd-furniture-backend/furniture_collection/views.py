from .models import Coleccion, Mueble
from .serializers import ColeccionSerializer, MuebleSerializer
from general_permissions.permissions import IsPermittedRBAC
from rest_framework import generics,permissions

class ColeccionListCreateView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Coleccion.objects.all()
    serializer_class = ColeccionSerializer

class ColeccionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Coleccion.objects.all()
    serializer_class = ColeccionSerializer

class MuebleListCreateView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Mueble.objects.all()
    serializer_class = MuebleSerializer

class MuebleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated, IsPermittedRBAC,)
    queryset = Mueble.objects.all()
    serializer_class = MuebleSerializer
