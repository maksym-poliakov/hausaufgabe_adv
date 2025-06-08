from django.db import models

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

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(help_text='название задачи')
    description = models.TextField(help_text='Описание задачи')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(choices=choices_status, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=70,help_text='Название категории')


    def __str__(self):
        return self.name