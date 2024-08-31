from django.contrib import admin
from .models import Profile, Task, ActivityLog

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'user_type')
    search_fields = ('user__username', 'name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'description')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'method', 'timestamp')
    list_filter = ('method', 'timestamp')
    search_fields = ('user__username', 'endpoint')
