from rest_framework import permissions

class AdminOrSuperuserPermission(permissions.BasePermission):
    """
    Custom permission class to allow access only to admin or superuser users.
    In our case, we'll need this when creating, updating or deleting products.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin_user())
