# reservas/views.py
from rest_framework import generics
from general_permissions.permissions import IsPermittedRBAC
from .models import ReservaMaterial, ReservaLugarFabricacion,MaterialEntregado
from .serializers import ReservaMaterialSerializer, ReservaLugarFabricacionSerializer,MaterialEntregadoSerializer
from rest_framework import permissions
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from furniture_collection.models import Coleccion
from drf_yasg import openapi
from ljj_muebles import settings


class ReservaMaterialListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = ReservaMaterial.objects.all()
    serializer_class = ReservaMaterialSerializer


class ReservaMaterialCreateView(APIView):
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id_venta_proveedor': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='The ID of the material supplied by a specific supplier.',
            ),
            'cantidad_pactada': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Cantidad de material a reservar.',
            ),
            'sede_entrega': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Sede a la cual se va a entregar.',
            ),
            'id_coleccion': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Id de la coleccion a la que pertenece.',
            ),
            'fecha_entrega_pactada': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Fecha de entrega pactada.',
            ),
        },
    ),
    responses={
        201: ReservaMaterialSerializer,
        # Add other possible responses as needed
    }
)   
    def post(self, request, format=None):
        id_venta_proveedor = request.data.get('id_venta_proveedor')
        cantidad = request.data.get('cantidad_pactada')
        sede_entrega = request.data.get('sede_entrega')
        id_coleccion = request.data.get("id_coleccion")
        fecha_entrega_pactada=request.data.get("fecha_entrega_pactada")
        # Make a request to the other application's API to get the supplier's ID
        
        supplier_api_url = f'http://{settings.API_PROVEEDORES_URL}:8000/api/proveedores/actor-materials/{id_venta_proveedor}/'
        response = requests.get(supplier_api_url)

        if response.status_code == status.HTTP_200_OK:
            supplier_data = response.json()
            if supplier_data.get('cantidad_disponible') >= cantidad and cantidad > 0:
                # Extract the supplier's ID from the response
                supplier_id = supplier_data.get('id')
                proveedor = supplier_data.get('actor_nombre')
                material = supplier_data.get('material_nombre')
                sede=sede_entrega
                coleccion=Coleccion.objects.get(id=id_coleccion)
                reserva_material = ReservaMaterial.objects.create(id_venta_proveedor=supplier_id,
                                                                nombre_proveedor=proveedor,nombre_material=material,
                                                                cantidad_pactada=cantidad,fecha_entrega_pactada=fecha_entrega_pactada,
                                                                sede_a_entregar=sede,coleccion=coleccion)
                serializer = ReservaMaterialSerializer(reserva_material)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("No existe tal cantidad para reservar", status=status.HTTP_400_BAD_REQUEST)
        return Response(response.json(), status=response.status_code)

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
    
class MaterialEntregadoListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsPermittedRBAC,)
    queryset = MaterialEntregado.objects.all()
    serializer_class = MaterialEntregadoSerializer
