from datetime import datetime,timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django_hausaufgabe_2.models import Task,SubTask
from django.db.models import Q, F,Value
# Create your views here.

def create_task(request):
    deadline = datetime.now().date() + timedelta(days=3)
    Task.objects.create(title="Prepare presentation",description="Prepare materials and slides for the presentation",
                        status="New",deadline=deadline)
    return HttpResponse('<h1>create task</h1>')


def create_subtask(request):
    task = Task.objects.get(title='Prepare presentation')
    deadline_1 = datetime.now().date() + timedelta(days=2)
    deadline_2 = datetime.now().date() + timedelta(days=1)
    sub_task_1 = SubTask(task=task,title="Gather information",
                         description="Find necessary information for the presentation",status="New",deadline=deadline_1)

    sub_task_2 = SubTask(task=task,title='Create slides',description="Create presentation slides",
                         status="New",deadline=deadline_2)


    sub_tasks = [sub_task_1,sub_task_2]
    SubTask.objects.bulk_create(sub_tasks)

    return HttpResponse('<h1>create_subtask</h1>')


def read_task_status(request):
    tasks_filter = Task.objects.filter(status="New")
    str_tasks = ''
    for task in tasks_filter:
        str_tasks += task.title + " " + task.status + ' | '

    return  HttpResponse(f'<h1>{str_tasks}</h1>')


def read_subtask_status(request):
    sub_task_filter = SubTask.objects.filter(Q(status='Done') & Q(deadline__lt=datetime.now().date()))
    str_subtask = ''
    for subtask in sub_task_filter:
        str_subtask += subtask.title + " " + subtask.status + ' | '

    return  HttpResponse(f'<h1>{str_subtask}</h1>')


def task_update(request):
    Task.objects.filter(title='Prepare presentation').update(status=Value("In progress"))
    SubTask.objects.filter(title="Gather information").update(deadline=F('deadline') - timedelta(days=2) )
    SubTask.objects.filter(title='Create slides').update(description=Value("Create and format presentation slides"))

    return HttpResponse('<h1>Tasks Update</h1>')


def delete_task(request):
    Task.objects.filter(title='Prepare presentation').delete()
    return HttpResponse('<h1>Task Delete</h1>')
