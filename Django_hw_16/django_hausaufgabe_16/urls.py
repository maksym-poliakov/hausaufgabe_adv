from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django_hausaufgabe_16.views import (

  SubTaskListCreateView,
  SubTaskRetrieveUpdateDestroyAPIView,
  TaskListCreateView,
  TaskRetrieveUpdateDestroyView,
  CategoryViewSet,
)
router = DefaultRouter()
router.register(r'category',CategoryViewSet)

urlpatterns = [
    # path('task_create/',view=task_create, name='task-create'),
    path('tasks/', view=TaskListCreateView.as_view(), name='list-tasks'),
    path('task/<int:pk>', view=TaskRetrieveUpdateDestroyView.as_view(), name='task'),
    path('',include(router.urls)),
    path('subtasks/', view=SubTaskListCreateView.as_view(), name='subtasks'),
    path('subtask/<int:pk>', view=SubTaskRetrieveUpdateDestroyAPIView.as_view(),
         name='subtask-detail-update-delete'),
]