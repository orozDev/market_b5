from rest_framework import permissions

from store.models import Product


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, product: Product):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user == product.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return request.method in permissions.SAFE_METHODS or request.user.is_superuser
