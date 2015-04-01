from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if  request.user.is_authenticated():
            return False

        return True