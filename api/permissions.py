from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    
    """
    Permission that allows access to superusers or the owner of the object.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user == view.get_object().user
        except:
            return request.user == view.get_object().author


class IsOwner(permissions.BasePermission):
    
    """
    Permission that allows access to the owner of the object.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user == view.get_object().user
        except:
            return request.user == view.get_object().author
