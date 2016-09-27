from rest_framework import permissions
from .utils import CheckUserAccess

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


class HasIpAccess(permissions.BasePermission):
    """
    check user location and ip
    """
    message = ""

    def has_permission(self, request, view):
        if request.method == 'POST':
            if not hasattr(view, 'log_action'):
                raise Exception('Please dd log_action to use this permission')
            action = view.log_action
            checker = CheckUserAccess(action, request)
            access, self.message = checker.check_access
            return access
        else:
            return True
