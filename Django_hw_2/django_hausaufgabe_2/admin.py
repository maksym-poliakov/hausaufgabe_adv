from django.contrib import admin
from django_hausaufgabe_2.models import Task,SubTask,Category
# Register your models here.

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','publish_date','status','deadline','created_at')
    search_fields = ('title','status','deadline','created_at')
    ordering = ['-created_at']
    list_per_page = 25


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title','task','status','deadline','created_at')
    search_fields = ('title','task','status','deadline','created_at')
    ordering = ['-created_at']
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

