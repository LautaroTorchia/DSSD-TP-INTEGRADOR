from django.urls import path
from .views import ActorListCreateView, MaterialListCreateView, ActorMaterialListCreateView,PossibleActorsForMaterialView
from .views import ActorMaterialRetrieveUpdateView,LugarDeFabricacionListCreateView,LugarDeFabricacionRetrieveUpdateView
from .views import LugarDeFabricacionEnReservaListCreateView, LugarDeFabricacionEnReservaRetrieveUpdateView

urlpatterns = [
    path('proveedores/', ActorListCreateView.as_view(), name='actor-list-create'),
    
    path('materiales/', MaterialListCreateView.as_view(), name='material-list-create'),
    
    path('proveedores-materiales/', ActorMaterialListCreateView.as_view(), name='actor-material-list-create'),
    path('actor-materials/<int:pk>/', ActorMaterialRetrieveUpdateView.as_view(), name='actor-material-delete'),
    
    path('<int:material_id>/', PossibleActorsForMaterialView.as_view(), name='possible-actors-for-material'),
    path('lugar-fabricacion/',LugarDeFabricacionListCreateView.as_view(), name='lugar-fabricacion'),
    path('lugar-fabricacion/<int:pk>/',LugarDeFabricacionRetrieveUpdateView.as_view(), name='lugar-fabricacion-detail'),
    path('lugar-fabricacion-en-reserva/', LugarDeFabricacionEnReservaListCreateView.as_view(), name='lugares-de-fabricacion-en-reserva-list-create'),
    path('lugar-fabricacion-en-reserva/<int:pk>/', LugarDeFabricacionEnReservaRetrieveUpdateView.as_view(), name='lugares-de-fabricacion-en-reserva-detail'),


]