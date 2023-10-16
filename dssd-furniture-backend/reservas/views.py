# reservas/views.py
from rest_framework import generics
from general_permissions.permissions import IsPermittedRBAC
from .models import ReservaMaterial, ReservaLugarFabricacion
from .serializers import ReservaMaterialSerializer, ReservaLugarFabricacionSerializer
from rest_framework import permissions

class ReservaMaterialListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ReservaMaterial.objects.all()
    serializer_class = ReservaMaterialSerializer

class ReservaLugarFabricacionListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ReservaLugarFabricacion.objects.all()
    serializer_class = ReservaLugarFabricacionSerializer
    
class ReservaMaterialDestroyView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ReservaMaterial.objects.all()
    serializer_class = ReservaMaterialSerializer

class ReservaLugarFabricacionDestroyView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ReservaLugarFabricacion.objects.all()
    serializer_class = ReservaLugarFabricacionSerializer