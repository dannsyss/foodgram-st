from rest_framework import permissions
# Сделал импорты поприятнее


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Доступно Автору или для чтения"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
