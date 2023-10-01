from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'upload', views.UploadViewSet, basename="upload")
router.register(r'upload-user-role', views.UserRoleUploadViewSet, basename="upload-user-role")
router.register(r'upload-view-descriptor', views.ViewDescriptorUploadViewSet, basename="upload-view-descriptor")
router.register(r'upload-view-descriptor', views.PermissionRoleUploadViewSet, basename="permission-role")
urlpatterns = [
    path('role', views.RoleListAPIView.as_view(), name="role"),    
    path('role/<int:id>/', views.RoleDetailAPIView.as_view(), name="role"),
    path('list/', views.RoleListView.as_view(), name="role-search"),
    path('roles/', include(router.urls)),
    path('role/register-role/', views.RoleAPIView.as_view(), name= "role"),
    path('user-role', views.UserRoleListAPIView.as_view(), name="user-role"),    
    path('user-role/<int:id>/', views.UserRoleDetailAPIView.as_view(), name="user-role"),
    path('user-role-list/', views.UserRoleListView.as_view(), name="user-role-search"),
    path('user-roles/', include(router.urls)),
    path('user-role/register-user-role/', views.UserRoleAPIView.as_view(), name= "user-role"),
    path('view-descriptor', views.ViewDescriptorListAPIView.as_view(), name="view-descriptor"),    
    path('view-descriptor/<int:id>/', views.ViewDescriptorDetailAPIView.as_view(), name="view-descriptor"),
    path('view-descriptor-list/', views.ViewDescriptorListView.as_view(), name="view-descriptor-search"),
    path('view-descriptors/', include(router.urls)),
    path('view-descriptor/register-view-descriptor/', views.ViewDescriptorAPIView.as_view(), name= "view-descriptor"),
    path('permission-role', views.PermissionRoleListAPIView.as_view(), name="permission-role"),    
    path('permission-role/<int:id>/', views.PermissionRoleDetailAPIView.as_view(), name="permission-role"),
    path('permission-role-list/', views.PermissionRoleListView.as_view(), name="permission-role-search"),
    path('permission-roles/', include(router.urls)),
    path('permission-role/register-permission-role/', views.PermissionRoleAPIView.as_view(), name= "permission-role"),
]