from rest_framework import permissions

class IsVendedor(permissions.BasePermission):
    """
    Permitir acceso a usuarios con rol distribuidor o vendedor
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            hasattr(request.user, 'rol') and
            request.user.rol and
            request.user.rol.lower() in ['vendedor', 'distribuidor']
        )


class IsAdministrador(permissions.BasePermission):
    """
    Permitir acceso solo a usuarios con rol administrador
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            hasattr(request.user, 'rol') and
            request.user.rol and
            request.user.rol.lower() == 'administrador'
        )


class IsComprador(permissions.BasePermission):
    """
    Permitir acceso solo a usuarios con rol comprador
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            hasattr(request.user, 'rol') and
            request.user.rol and
            request.user.rol.lower() == 'comprador'
        )