from rest_framework.permissions import BasePermission

class IsAdminOrSecretario(BasePermission):
    """Permite acceso solo a usuarios con rol 'admin' o 'secretario'."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'rol', None) in ['admin', 'secretario'])
