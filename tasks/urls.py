from django.urls import path
from .views import TaskListCreateView, TaskDetailView, ActivityLogListView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('activity-logs/', ActivityLogListView.as_view(), name='activity-log-list'),
]
