from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    
    """
    Permission that allows access to superusers or the owner of the object.
    """
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user

class IsOwner(permissions.BasePermission):
    
    """
    Permission that allows access to the owner of the object.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user