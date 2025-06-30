from django.urls import path
from django_hausaufgabe_12.views import (
  task_create,
  list_tasks,
  get_task,
  tasks_statistics
)

urlpatterns = [
    path('task_create/',view=task_create, name='task-create'),
    path('tasks_list/',view=list_tasks, name='list-tasks'),
    path('task/<int:pk>',view=get_task, name='task'),
    path('statistics', view=tasks_statistics, name='statistics')
]