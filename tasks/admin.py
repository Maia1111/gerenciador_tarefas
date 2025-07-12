from django.contrib import admin
from .models import Task, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color', 'icon', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    ordering = ('-created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'completed', 'due_date', 'created_at')
    list_filter = ('completed', 'priority', 'category', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
