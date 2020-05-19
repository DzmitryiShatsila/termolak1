from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.AllTasks.as_view(), name='all-tasks'),
    path('<str:id>/done', views.task_done, name='done'),
    path('<str:id>/move_back', views.task_move_back, name='move-back'),
    path('tasks_update/<str:slug>', views.TaskUpdate.as_view(), name='task-update'),
    path('tasks_delete/<str:slug>', views.TaskDelete.as_view(), name='task-delete'),
]