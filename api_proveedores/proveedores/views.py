from rest_framework import generics
from .models import Actor, Material, ActorMaterial,LugarDeFabricacion,LugarDeFabricacionEnReserva
from .serializers import ActorSerializer, MaterialSerializer, ActorMaterialSerializer,LugarDeFabricacionSerializer,LugarDeFabricacionEnReservaSerializer
from rest_framework import generics

class LugarDeFabricacionListCreateView(generics.ListCreateAPIView):
    queryset = LugarDeFabricacion.objects.all()
    serializer_class = LugarDeFabricacionSerializer

class LugarDeFabricacionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
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


class ActorMaterialRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ActorMaterial.objects.all()
    serializer_class = ActorMaterialSerializer


class LugarDeFabricacionEnReservaListCreateView(generics.ListCreateAPIView):
    queryset = LugarDeFabricacionEnReserva.objects.all()
    serializer_class = LugarDeFabricacionEnReservaSerializer

class LugarDeFabricacionEnReservaRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = LugarDeFabricacionEnReserva.objects.all()
    serializer_class = LugarDeFabricacionEnReservaSerializer
