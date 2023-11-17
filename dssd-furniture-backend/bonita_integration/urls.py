# bonita_integration/urls.py

from django.urls import path
from .views import BonitaCheckProcesses,BonitaInstantiateProcess,BonitaUserTasks,BonitaExecuteUserTask,BonitaCaseVariable,BonitaUpdateCaseVariable,BonitaArchivedTasksView

urlpatterns = [
    
    path('list-processes/',BonitaCheckProcesses.as_view(),name='bonita-list-processes'),
    path('instantiate/<int:process_id>/', BonitaInstantiateProcess.as_view(), name='bonita-instantiate-process'),
    path('user-tasks/', BonitaUserTasks.as_view(), name='bonita-user-tasks'),
    path('execute-user-task/<int:task_id>/', BonitaExecuteUserTask.as_view(), name='execute-user-task'),
    path('case-variable/<int:id_instancia>/<str:variablename>/', BonitaCaseVariable.as_view(), name='bonita-case-variable'),
    path('update-case-variable/<int:id_instancia>/<str:variablename>/', BonitaUpdateCaseVariable.as_view(), name='bonita-update-case-variable'),
    path('archived-tasks/', BonitaArchivedTasksView.as_view(), name='bonita-user-tasks'),
]