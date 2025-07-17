from rest_framework import serializers
from .validated import validated_name,validate_deadline
from .models import (
    Task,
    Category,
    SubTask
)


class TaskCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True)
    deadline = serializers.DateTimeField(validators=[validate_deadline])
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'categories','deadline']

class TaskListSerializer(TaskCreateSerializer):
    pass

class TaskGetSerializer(TaskCreateSerializer):
    pass

class TasksStatisticsSerializer(serializers.Serializer):

    total_number_of_tasks = serializers.IntegerField()
    number_of_tasks_status = serializers.IntegerField()
    number_of_overdue_tasks = serializers.IntegerField()


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = ['id','title','description','task','status','deadline','created_at']


class SubTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id','title','description','task','status','deadline','created_at']


class SubTaskListSerializer(serializers.ModelSerializer):
    task = TaskCreateSerializer()
    class Meta:
        model = SubTask
        fields = ['id','title', 'description', 'task', 'status', 'deadline', 'created_at']



class SubTaskDetailSerializer(serializers.ModelSerializer):
    task = TaskCreateSerializer()
    class Meta:
        model = SubTask
        fields = ['id','title', 'description', 'task', 'status', 'deadline', 'created_at']


class SubTaskUpdateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    class Meta:
        model = SubTask
        fields = ['id','title','description','task','status','deadline']


class CategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validated_name])
    class Meta:
        model = Category
        fields = ['id','name']

    def create(self,validated_data):
        return Category.objects.create(**validated_data)


class CategoryUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validated_name])

    class Meta:
        model = Category
        fields = ['id','name']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance



class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTasksSerializer(many=True,read_only=True)

    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'categories','deadline','subtasks']
