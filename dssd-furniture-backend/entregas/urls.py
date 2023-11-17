from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.OrdenDeEntregaListCreateView.as_view(), name='orden-list'),
    path('ordenes/<int:pk>/', views.OrdenDeEntregaRetrieveUpdateDestroyView.as_view(), name='orden-detail'),
    path('lotes-fabricados/', views.LotesFabricadosListCreateView.as_view(), name='lotes-fabricados-list-create'),
    path('lugares-de-distribucion/', views.LugarDeDistribucionListCreateView.as_view(), name='lugares-de-distribucion-list-create'),
    path('vendedores-finales/', views.VendedorFinalListCreateView.as_view(), name='vendedores-finales-list-create'),
    path('orden-de-lote/', views.AsociacionLoteOrdenEntregaListCreateView.as_view(), name='asociaciones-lote-orden-entrega-list-create')
]
