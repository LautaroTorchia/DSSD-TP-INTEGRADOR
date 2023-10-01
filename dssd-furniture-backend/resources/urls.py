from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'upload', views.UploadViewSet, basename="upload")
router.register(r'upload', views.ConfigResourceUploadViewSet, basename="upload-config-resource")
urlpatterns = [
    path('', views.ResourceListAPIView.as_view(), name="resource"),    
    path('<int:id>', views.ResourceDetailAPIView.as_view(), name="resource"),
    path('list', views.ResourceListView.as_view(), name="resource-search"),
    path('config-resource/', views.ConfigResourceListAPIView.as_view(), name="config-resource"),    
    path('config-resource/<int:id>', views.ConfigResourceDetailAPIView.as_view(), name="config-resource"),
    path('config-resource/list', views.ConfigResourceListView.as_view(), name="config-resource-search"),
    path('check-config-resource/', views.ConfigResourceCheckView.as_view(), name="config-resource-check"),
    path('config-message/', views.ConfigMessageListAPIView.as_view(), name="config-message"),
    path('config-message/list', views.ConfigMessageListView.as_view(), name="config-message-search"),
    path('config-message/<int:id>', views.ConfigMessageDetailAPIView.as_view(), name="config-message"),
    path('resources/', include(router.urls)),
]
