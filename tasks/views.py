from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Task, ActivityLog, Profile
from .serializers import TaskSerializer, ActivityLogSerializer
from .permissions import IsAdminUser, IsClientUser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task, Profile
from .serializers import TaskSerializer
from .permissions import IsAdminUser, IsClientUser

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)

        # Admin users see all tasks; clients see only their own tasks
        if profile.user_type == 'admin':
            return Task.objects.all()
        else:
            return Task.objects.filter(user=profile)

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)



class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")

    def get(self, request, pk):
        user_profile = request.user.profile
        if user_profile.user_type == 'admin':
            task = get_object_or_404(Task, pk=pk)  # Admins can access all tasks
        else:
            task = self.get_object(pk, user_profile)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        user_profile = request.user.profile
        if user_profile.user_type == 'admin':
            task = get_object_or_404(Task, pk=pk)  # Admins can update any task
        else:
            task = self.get_object(pk, user_profile)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_profile = request.user.profile
        if user_profile.user_type == 'admin':
            task = get_object_or_404(Task, pk=pk)  # Admins can delete any task
        else:
            task = self.get_object(pk, user_profile)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ActivityLogListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Check if the user has a profile and if the user type is 'admin'
        try:
            if not request.user.profile.user_type == 'admin':
                raise PermissionDenied("You do not have permission to access activity logs.")
        except Profile.DoesNotExist:
            raise PermissionDenied("User profile does not exist.")

        # Fetch all activity logs
        logs = ActivityLog.objects.all()
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data)