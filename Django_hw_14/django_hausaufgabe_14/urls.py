from django.urls import path
from django_hausaufgabe_14.views import (
  task_create,
  get_task,
  tasks_statistics,
  category_create,
  category_update,
  task_detail,
  SubTaskListCreateView,
  SubTaskDetailUpdateDeleteView,
  TaskListView,
)

urlpatterns = [
    path('task_create/',view=task_create, name='task-create'),
    path('tasks_list/',view=TaskListView.as_view(), name='list-tasks'),
    path('task/<int:pk>',view=get_task, name='task'),
    path('statistics/', view=tasks_statistics, name='statistics'),
    path('category_create/',view=category_create, name='category-create'),
    path('category_update/<int:pk>',view=category_update, name='category-update'),
    path('task_detail/<int:pk>',view=task_detail,name='task-detail'),
    path('subtasks/',view=SubTaskListCreateView.as_view(),name='subtasks'),
    path('subtasks/<int:pk>',view=SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),


]