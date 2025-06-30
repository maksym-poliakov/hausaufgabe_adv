from rest_framework import serializers
from .models import Task,Category


class TaskCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True)
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'categories','deadline']

class TaskListSerializer(TaskCreateSerializer):
    pass

class TaskGetSerializer(TaskCreateSerializer):
    pass

class TasksStatisticsSerializer(serializers.Serializer):

    total_number_of_tasks = serializers.IntegerField()
    number_of_tasks_status = serializers.IntegerField()
    number_of_overdue_tasks = serializers.IntegerField()


