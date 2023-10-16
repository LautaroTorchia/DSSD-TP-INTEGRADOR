from django.urls import path
from .views import ReservaMaterialListCreateView, ReservaLugarFabricacionListCreateView, \
    ReservaMaterialDestroyView, ReservaLugarFabricacionDestroyView

urlpatterns = [
    path('reservas-materiales/', ReservaMaterialListCreateView.as_view(), name='reserva-material-list-create'),
    path('reservas-lugares-fabricacion/', ReservaLugarFabricacionListCreateView.as_view(), name='reserva-lugar-fabricacion-list-create'),
    path('reservas-materiales/<int:pk>/', ReservaMaterialDestroyView.as_view(), name='reserva-material-destroy'),
    path('reservas-lugares-fabricacion/<int:pk>/', ReservaLugarFabricacionDestroyView.as_view(), name='reserva-lugar-fabricacion-destroy'),
]