from django.contrib import admin
from .models import Task, Category

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','status', 'due_date', 'order')
    list_filter = ('status',)
    ordering = ('status', 'order')

admin.site.register(Category)

