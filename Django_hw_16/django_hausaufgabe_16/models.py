from django.db import models
from django.utils import timezone
from .managers import SoftDeleteManager
# Create your models here.
choices_status = [
    ('New','New'),
    ('In progress','In progress'),
    ('Pending','Pending'),
    ('Blocked','Blocked'),
    ('Done','Done'),
]

class Task(models.Model):

    title = models.CharField(unique_for_date='publish_date', help_text='название задачи')
    publish_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(help_text='Описание задачи')
    categories = models.ManyToManyField('Category', related_name='tasks',help_text='Категория задачи')
    status = models.CharField(choices=choices_status,default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = ('title',)


    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(help_text='название задачи')
    description = models.TextField(help_text='Описание задачи')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(choices=choices_status, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Sub Task'
        verbose_name_plural = 'Sub Tasks'
        unique_together = ('title',)


    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=70,help_text='Название категории')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('name',)

    objects = SoftDeleteManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


    def __str__(self):
        return self.name