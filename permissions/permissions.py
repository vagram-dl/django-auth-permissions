from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user_role_name = getattr(request.user.role, 'name',None)
        return request.user.is_authenticated and user_role_name == "Admin"