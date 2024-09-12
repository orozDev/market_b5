from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):

        print('...')

        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )