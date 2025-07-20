from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .serializers import (
    TaskListCreateSerializer,
    TaskRetrieveUpdateDestroySerializer,
    CategorySerializer,
    SubTaskListCreateSerializer,
    SubtaskRetrieveUpdateDestroySerializer,
)
from .models import Task,Category,SubTask
# Create your views here.
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListCreateSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    filterset_fields = ['status','deadline']

    def list(self, request, *args, **kwargs):
        filters = {}
        created_at_week_day = request.query_params.get('weekday')

        if created_at_week_day:
            filters['created_at__week_day'] = int(created_at_week_day)

        queryset = self.get_queryset()

        if filters:
            queryset = queryset.filter(**filters)

        queryset = self.filter_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskRetrieveUpdateDestroySerializer



class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskListCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title','description']
    filterset_fields = ['status','deadline']
    ordering_fields = ['created_at']
    pagination_class = CustomPagination
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


    def list(self, request, *args, **kwargs) -> Response:

        queryset = self.get_queryset()

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubtaskRetrieveUpdateDestroySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    @action(detail=False, methods=['get'])
    def count_tasks(self,request):
        count_tasks_in_category = Category.objects.annotate(tasks_count=Count('tasks'))

        data = [
            {
            "id": category.id,
            "category": category.name,
            "tasks_count":category.tasks_count,
            }
            for category in count_tasks_in_category
        ]

        return Response(data)
# @api_view(['GET'])
# def tasks_statistics(request):
#
#     total_number_of_tasks = Task.objects.aggregate(total_number_of_tasks=Count('id'))
#     number_of_tasks_status = Task.objects.values('status').annotate(count=Count('id')).order_by('status')
#     number_of_overdue_tasks = Task.objects.aggregate(overdue_tasks=Count('id',
#                                                                          filter=Q(deadline__lt=timezone.now())))
#
#     data = {
#         'total_number_of_tasks':total_number_of_tasks,
#         'number_of_tasks_status':number_of_tasks_status,
#         'number_of_overdue_tasks':number_of_overdue_tasks
#     }
#
#     return Response(data,status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# def category_create(request):
#     serializer = CategoryCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['POST'])
# def category_update(request,pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return Response({'errors: Category not found'},status=status.HTTP_404_NOT_FOUND)
#     serializer = CategoryUpdateSerializer(category, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


