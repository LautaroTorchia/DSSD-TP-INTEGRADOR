from rest_framework import generics
from .models import Actor, Material, ActorMaterial
from .serializers import ActorSerializer, MaterialSerializer, ActorMaterialSerializer
from rest_framework import generics,permissions
from general_permissions.permissions import IsPermittedRBAC
from django.http import HttpResponse
from rest_framework import status

class ActorListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class MaterialListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ActorMaterialListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ActorMaterial.objects.all()
    serializer_class = ActorMaterialSerializer

class PossibleActorsForMaterialView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    serializer_class = ActorMaterialSerializer

    def get_queryset(self):
        material_id = self.kwargs.get('material_id')
        return ActorMaterial.objects.filter(material=material_id)

#delete views:
class ActorDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Actor.objects.all()

class MaterialDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = Material.objects.all()

class ActorMaterialDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ActorMaterial.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)