# bonita_integration/urls.py

from django.urls import path
from .views import BonitaLogin,BonitaCheckProcesses,BonitaInstantiateProcess,BonitaUserTasks,BonitaExecuteUserTask

urlpatterns = [
    path('login/', BonitaLogin.as_view(), name='bonita-login'),
    path('list-processes/',BonitaCheckProcesses.as_view(),name='bonita-list-processes'),
    path('bonita/instantiate/<int:process_id>/', BonitaInstantiateProcess.as_view(), name='bonita-instantiate-process'),
    path('bonita/user-tasks/', BonitaUserTasks.as_view(), name='bonita-user-tasks'),
    path('execute-user-task/<int:task_id>/', BonitaExecuteUserTask.as_view(), name='execute-user-task'),
]