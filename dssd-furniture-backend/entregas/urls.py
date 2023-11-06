from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.OrdenDeEntregaListCreateView.as_view(), name='orden-list'),
    path('ordenes/<int:pk>/', views.OrdenDeEntregaRetrieveUpdateDestroyView.as_view(), name='orden-detail'),
]
