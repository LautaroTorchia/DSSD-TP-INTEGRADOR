"""ljj_muebles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

schema_view = get_schema_view(
    openapi.Info(
        title="API LJJMuebles",
        default_version='v1',
        description="API de operaciones de LJJMuebles",
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #Django admin
    path('api/admin/', admin.site.urls),
    
    #Swagger endpoints
    path('api/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
    path('api/redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),

    #User endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/authorization/', include('authorization.urls')),
    
    
    #Functional endpoints
    path('api/coleccion/', include('furniture_collection.urls')),
    path('api/bonita/', include('bonita_integration.urls')),
    path('api/reservas/',include('reservas.urls')),
    path('api/entregas/',include('entregas.urls'))
]
