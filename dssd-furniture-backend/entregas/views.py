from rest_framework import generics
from .models import OrdenDeEntrega,LotesFabricados,SedeDeDistribucion,VendedorFinal,AsociacionLoteOrdenEntrega
from .serializers import OrdenDeEntregaSerializer,LotesFabricadosSerializer,LugarDeDistribucionSerializer,VendedorFinalSerializer,AsociacionLoteOrdenEntregaSerializer
from general_permissions.permissions import IsPermittedRBAC
from rest_framework import permissions

class OrdenDeEntregaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = OrdenDeEntrega.objects.all()
    serializer_class = OrdenDeEntregaSerializer

class OrdenDeEntregaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = OrdenDeEntrega.objects.all()
    serializer_class = OrdenDeEntregaSerializer

class LotesFabricadosListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = LotesFabricados.objects.all()
    serializer_class = LotesFabricadosSerializer

class LugarDeDistribucionListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = SedeDeDistribucion.objects.all()
    serializer_class = LugarDeDistribucionSerializer

class VendedorFinalListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = VendedorFinal.objects.all()
    serializer_class = VendedorFinalSerializer

class AsociacionLoteOrdenEntregaListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = AsociacionLoteOrdenEntrega.objects.all()
    serializer_class = AsociacionLoteOrdenEntregaSerializer