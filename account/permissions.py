import logging

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .utils import CheckUserAccess

logger = logging.getLogger('account.permissions')


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow users that are NOT logged in.
    This is used for things like the registration + login pages.
    """
    message = "You must be logged in to perform this action."

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
    # Default message -
    # will be overridden by a more specific one below.
    message = "Unable to verify your location."

    def has_permission(self, request, view):
        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.can_bypass_location_check') and \
                request.user.is_authenticated():
            logger.info(
                'User: %s has bypassed the location check via permissions.' % request.user.username)
            return True

        checker = CheckUserAccess(request)
        # Set the response error message to whatever our checker returns.
        access, reason = checker.check_access
        self.message = {
            'detail': reason,
            'status': 'IP_CHECK_FAILED'
        }

        # We can't just return False here because of a strange DRF behavior.
        # If you return False on a custom permission, it ignores the message you set and
        # returns a hard "No permissions" message that you cannot change.
        # Instead we manually set our response body and throw the 403.
        if access is False:
            raise PermissionDenied(detail=self.message)

        # `access` is a bool that tells us if the user passed our IP location+proxy checks.
        return access


class HasVerifiedIdentity(permissions.BasePermission):
    """
    Has the user verified their identity with GIDX? If they have there will be a
    user.identity model.
    """
    message = "You must verify your identity to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if hasattr(request.user, 'information') is False:
            return False

        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.can_bypass_identity_verification'):
            logger.info(
                'User: %s has bypassed the identity check via permissions.' % request.user.username)
            return True

        # Check if their identity is verified.
        return request.user.information.has_verified_identity
