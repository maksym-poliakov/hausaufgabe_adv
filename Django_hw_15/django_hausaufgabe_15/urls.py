from django.urls import path
from django_hausaufgabe_15.views import (
  tasks_statistics,
  category_create,
  category_update,
  SubTaskListCreateView,
  SubTaskRetrieveUpdateDestroyAPIView,
  TaskListCreateView,
  TaskRetrieveUpdateDestroyView,
)

urlpatterns = [
    # path('task_create/',view=task_create, name='task-create'),
    path('tasks/', view=TaskListCreateView.as_view(), name='list-tasks'),
    path('task/<int:pk>', view=TaskRetrieveUpdateDestroyView.as_view(), name='task'),
    path('statistics/', view=tasks_statistics, name='statistics'),
    path('category_create/',view=category_create, name='category-create'),
    path('category_update/<int:pk>',view=category_update, name='category-update'),
    path('subtasks/', view=SubTaskListCreateView.as_view(), name='subtasks'),
    path('subtask/<int:pk>', view=SubTaskRetrieveUpdateDestroyAPIView.as_view(),
         name='subtask-detail-update-delete'),
]