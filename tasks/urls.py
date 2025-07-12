from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView, debug_categories,
    toggle_task_status, quick_add_task, update_task_position
)

urlpatterns = [
    # Task URLs
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('debug-categories/', debug_categories, name='debug_categories'),
    
    # AJAX URLs
    path('<int:task_id>/toggle-status/', toggle_task_status, name='toggle_task_status'),
    path('quick-add/', quick_add_task, name='quick_add_task'),
    path('update-positions/', update_task_position, name='update_task_position'),
] 