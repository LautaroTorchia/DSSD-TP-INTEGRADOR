from rest_framework import generics
from .models import Actor, Material, ActorMaterial,LugarDeFabricacion
from .serializers import ActorSerializer, MaterialSerializer, ActorMaterialSerializer,LugarDeFabricacionSerializer
from rest_framework import generics
from django.http import HttpResponse
from rest_framework import status

class LugarDeFabricacionListCreateView(generics.ListCreateAPIView):
    queryset = LugarDeFabricacion.objects.all()
    serializer_class = LugarDeFabricacionSerializer

class LugarDeFabricacionDestroyView(generics.DestroyAPIView):
    queryset = LugarDeFabricacion.objects.all()
    serializer_class = LugarDeFabricacionSerializer
    
class ActorListCreateView(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class MaterialListCreateView(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ActorMaterialListCreateView(generics.ListCreateAPIView):

    queryset = ActorMaterial.objects.all()
    serializer_class = ActorMaterialSerializer

class PossibleActorsForMaterialView(generics.ListAPIView):

    serializer_class = ActorMaterialSerializer

    def get_queryset(self):
        material_id = self.kwargs.get('material_id')
        return ActorMaterial.objects.filter(material=material_id)

#delete views:
class ActorDeleteView(generics.DestroyAPIView):
    queryset = Actor.objects.all()

class MaterialDeleteView(generics.DestroyAPIView):
    queryset = Material.objects.all()

class ActorMaterialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActorMaterial.objects.all()
    serializer_class = ActorMaterialSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)