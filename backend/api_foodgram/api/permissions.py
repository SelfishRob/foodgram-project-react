from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user and request.user.is_staff
        )
