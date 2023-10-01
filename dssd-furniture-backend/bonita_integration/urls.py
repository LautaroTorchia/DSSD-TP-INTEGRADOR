# bonita_integration/urls.py

from django.urls import path
from .views import BonitaLogin,BonitaCheckProcesses

urlpatterns = [
    path('login/', BonitaLogin.as_view(), name='bonita-login'),
    path('list-processes/',BonitaCheckProcesses.as_view(),name='bonita-list-processes')
]