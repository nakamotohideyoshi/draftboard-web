from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import exceptions
from .utils import CheckUserAccess
import logging

logger = logging.getLogger('django')


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow users that are NOT logged in.
    This is used for things like the registration + login pages.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated():
            return False

        return True


class HasIpAccess(permissions.BasePermission):
    """
    check user location and ip
    """

    def has_permission(self, request, view):
        # TODO: Figuring out best way to add default permissions, until then let all users
        # use the site.
        return True

        checker = CheckUserAccess(request)
        access, message = checker.check_access

        # If our IP check has determined we don't have access, return a 403.
        if not access:
            raise exceptions.PermissionDenied('IP_CHECK_FAILED')

        return True


class HasVerifiedIdentity(permissions.BasePermission):
    """
    Has the user verified their identity with Trulioo? If they have there will be a
    user.identity model.
    """
    def has_permission(self, request, view):
        is_verified = False
        try:
            is_verified = (request.user.identity is not None)
        except ObjectDoesNotExist:
            pass
        return is_verified
