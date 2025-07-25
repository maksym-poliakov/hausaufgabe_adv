from django.contrib import admin
from django_hausaufgabe_18.models import Task,SubTask,Category
# Register your models here.

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title','publish_date','status','deadline','created_at')
    search_fields = ('title','status','deadline','created_at')
    ordering = ['-created_at']
    list_per_page = 25
    inlines = [SubTaskInline]

    def short_title(self,obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        else:
            return obj.title

    short_title.short_description = "title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title','task','status','deadline','created_at')
    search_fields = ('title','task','status','deadline','created_at')
    ordering = ['-created_at']
    list_per_page = 25

    @admin.action(description = 'Update status Done')
    def done_status(self,req,queryset):
        queryset.update(status='Done')

    actions = [done_status]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



