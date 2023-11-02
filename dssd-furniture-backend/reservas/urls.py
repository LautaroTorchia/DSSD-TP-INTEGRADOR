from django.urls import path
from .views import ReservaMaterialListView, ReservaLugarFabricacionListCreateView, \
    ReservaMaterialDestroyView, ReservaLugarFabricacionDestroyView,ReservaMaterialCreateView, \
    LugarDeFabricacionListCreateView,LugarDeFabricacionDestroyView,MaterialEntregadoListCreateView

urlpatterns = [
    path('reservas-materiales/', ReservaMaterialListView.as_view(), name='reserva-material-list'),
    path('reservas-lugares-fabricacion/', ReservaLugarFabricacionListCreateView.as_view(), name='reserva-lugar-fabricacion-list-create'),
    path('reservas-materiales/<int:pk>/', ReservaMaterialDestroyView.as_view(), name='reserva-material-destroy'),
    path('reservas-lugares-fabricacion/<int:pk>/', ReservaLugarFabricacionDestroyView.as_view(), name='reserva-lugar-fabricacion-destroy'),
    path('reservar-material/', ReservaMaterialCreateView.as_view(), name='reserva-material-create'),
    path('lugar-fabricacion/', LugarDeFabricacionListCreateView.as_view(), name='lugar-fabricacion-list-create'),
    path('lugar-fabricacion/<int:pk>/', LugarDeFabricacionDestroyView.as_view(), name='lugar-fabricacion-destroy'),
    path('material-entregado/',MaterialEntregadoListCreateView.as_view(), name='material-entregado-list-view')
]