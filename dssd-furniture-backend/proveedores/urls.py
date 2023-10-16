from django.urls import path
from .views import ActorListCreateView, MaterialListCreateView, ActorMaterialListCreateView,PossibleActorsForMaterialView
from .views import MaterialDeleteView,ActorDeleteView,ActorMaterialDeleteView

urlpatterns = [
    path('proveedores/', ActorListCreateView.as_view(), name='actor-list-create'),
    path('proveedores/<int:pk>/', ActorDeleteView.as_view(), name='actor-delete'),
    
    path('materiales/', MaterialListCreateView.as_view(), name='material-list-create'),
    path('materiales/<int:pk>/', MaterialDeleteView.as_view(), name='material-delete'),
    
    path('proveedores-materiales/', ActorMaterialListCreateView.as_view(), name='actor-material-list-create'),
    path('actor-materials/<int:pk>/', ActorMaterialDeleteView.as_view(), name='actor-material-delete'),
    
    path('<int:material_id>/', PossibleActorsForMaterialView.as_view(), name='possible-actors-for-material'),
]