from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from .serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskGetSerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
    TaskDetailSerializer,
    SubTaskListSerializer,
    SubTaskCreateSerializer,
    SubTaskDetailSerializer,
    SubTaskUpdateSerializer,

)
from .models import Task,Category,SubTask
# Create your views here.

class SubTaskListCreateView(APIView):

    def get(self,request:Request) -> Response:
        subtasks = SubTask.objects.all()
        serializer = SubTaskListSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request:Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):

    def get(self,request: Request,pk) -> Response:
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist :
            return Response({'errors: SubTask not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskDetailSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request:Request,pk) -> Response:
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'errors: SubTask not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubTaskUpdateSerializer(subtask,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request: Request,pk) -> Response:
        try:
            subtask = SubTask.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'errors: SubTask not found'}, status=status.HTTP_400_BAD_REQUEST)

        subtask.delete()
        return Response({'message: SubTask is Deleted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_tasks(request):

    tasks = Task.objects.all()
    serializer = TaskListSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task(request,pk):

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error: Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskGetSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def tasks_statistics(request):

    total_number_of_tasks = Task.objects.aggregate(total_number_of_tasks=Count('id'))
    number_of_tasks_status = Task.objects.values('status').annotate(count=Count('id')).order_by('status')
    number_of_overdue_tasks = Task.objects.aggregate(overdue_tasks=Count('id',
                                                                         filter=Q(deadline__lt=timezone.now())))

    data = {
        'total_number_of_tasks':total_number_of_tasks,
        'number_of_tasks_status':number_of_tasks_status,
        'number_of_overdue_tasks':number_of_overdue_tasks
    }

    return Response(data,status=status.HTTP_200_OK)


@api_view(['POST'])
def category_create(request):
    serializer = CategoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def category_update(request,pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'errors: Category not found'},status=status.HTTP_404_NOT_FOUND)
    serializer = CategoryUpdateSerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def task_detail(request,pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'errors: Task not found'})

    serializer = TaskDetailSerializer(task)

    return Response(serializer.data, status=status.HTTP_200_OK)
