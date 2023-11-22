# reservas/views.py
from rest_framework import generics
from .models import ReservaMaterial, ReservaLugarFabricacion
from .serializers import ReservaMaterialSerializer, ReservaLugarFabricacionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from proveedores.models import ActorMaterial,LugarDeFabricacion


class ReservaMaterialListView(generics.ListAPIView):
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
            'fecha_entrega_pactada': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Fecha de entrega pactada.',
            ),
        },
    ),
    responses={
        201: ReservaMaterialSerializer,
    }
)   
    def post(self, request, format=None):
        id_venta_proveedor = request.data.get('id_venta_proveedor')
        cantidad = int(request.data.get('cantidad_pactada'))
        sede_entrega = request.data.get('sede_entrega')
        fecha_entrega_pactada=request.data.get("fecha_entrega_pactada")
        
        # Make a request to the other application's API to get the supplier's ID
        try:
            supplier_data=ActorMaterial.objects.get(id=int(id_venta_proveedor))
        except:
            return Response("No existe la venta que quiere reservar", status=status.HTTP_400_BAD_REQUEST)
        try:
            sede=LugarDeFabricacion.objects.get(id=int(sede_entrega))
        except:
            return Response("No existe la sede entrega indicada", status=status.HTTP_400_BAD_REQUEST)
        
        if supplier_data.cantidad_disponible >= cantidad and cantidad > 0:
            supplier_id = supplier_data.id
            reserva_material = ReservaMaterial.objects.create(id_venta_proveedor=supplier_data,
                                                            cantidad_pactada=cantidad,fecha_entrega_pactada=fecha_entrega_pactada,
                                                            sede_a_entregar=sede)
            serializer = ReservaMaterialSerializer(reserva_material)
            supplier_data.cantidad_disponible -= cantidad
            if supplier_data.cantidad_disponible == 0:
                supplier_data.delete()
            else:
                supplier_data.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("No existe tal cantidad para reservar", status=status.HTTP_400_BAD_REQUEST)

class ReservaLugarFabricacionListCreateView(generics.ListCreateAPIView):
    queryset = ReservaLugarFabricacion.objects.all()
    serializer_class = ReservaLugarFabricacionSerializer
    
class ReservaMaterialDestroyView(generics.DestroyAPIView):
    queryset = ReservaMaterial.objects.all()
    serializer_class = ReservaMaterialSerializer

class ReservaLugarFabricacionDestroyView(generics.DestroyAPIView):
    queryset = ReservaLugarFabricacion.objects.all()
    serializer_class = ReservaLugarFabricacionSerializer
    
