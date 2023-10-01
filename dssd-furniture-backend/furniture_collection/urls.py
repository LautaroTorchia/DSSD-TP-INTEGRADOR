from django.urls import path
from .views import ColeccionListCreateView, ColeccionRetrieveUpdateDestroyView, MuebleListCreateView, MuebleRetrieveUpdateDestroyView

urlpatterns = [
    path('', ColeccionListCreateView.as_view(), name='coleccion-list-create'),
    path('<int:pk>/', ColeccionRetrieveUpdateDestroyView.as_view(), name='coleccion-retrieve-update-destroy'),
    path('muebles/', MuebleListCreateView.as_view(), name='mueble-list-create'),
    path('muebles/<int:pk>/', MuebleRetrieveUpdateDestroyView.as_view(), name='mueble-retrieve-update-destroy'),
]