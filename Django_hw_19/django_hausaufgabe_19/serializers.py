from rest_framework import serializers
from .validated import validated_name,validate_deadline
from .models import (
    Task,
    Category,
    SubTask
)


class TaskListCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True)
    deadline = serializers.DateTimeField(validators=[validate_deadline])
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'owner','categories','deadline']



class TaskRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    deadline = serializers.DateTimeField(validators=[validate_deadline])

    class Meta:
        model = Task
        fields = ['id', 'description', 'status', 'owner', 'categories', 'deadline']




class TasksStatisticsSerializer(serializers.Serializer):

    total_number_of_tasks = serializers.IntegerField()
    number_of_tasks_status = serializers.IntegerField()
    number_of_overdue_tasks = serializers.IntegerField()


class SubTaskListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ['title','description','status','deadline','task']
        read_only_fields = ['id', 'owner', 'created_at']

class SubtaskRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'owner', 'status', 'deadline']



class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validated_name])
    class Meta:
        model = Category
        fields = ['id','name','is_deleted','deleted_at']

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

class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['owner']

