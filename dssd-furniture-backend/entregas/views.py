from rest_framework import generics
from .models import OrdenDeEntrega
from .serializers import OrdenDeEntregaSerializer
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
