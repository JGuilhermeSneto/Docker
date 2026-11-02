from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/status/', views.task_update_status, name='task_update_status'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('teoria/', views.theory_view, name='theory'),
    
    # JSON APIs
    path('api/system-info/', views.api_system_info, name='api_system_info'),
    path('api/tasks/', views.api_tasks, name='api_tasks'),
]

