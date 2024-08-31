from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.user_type == 'admin'

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.user_type == 'client'
