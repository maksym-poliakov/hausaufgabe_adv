from django.urls import path
from django_hausaufgabe_2.views import (
    create_task,
    create_subtask,
    read_task_status,
    read_subtask_status,
    task_update,
    delete_task
)
urlpatterns = [
    path('create_task',view=create_task),
    path('create_subtask', view=create_subtask),
    path('task_status',view=read_task_status),
    path('subtask_status', view=read_subtask_status),
    path('task_update', view=task_update),
    path('delete_task',view=delete_task)
]