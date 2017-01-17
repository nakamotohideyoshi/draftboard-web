import logging

from rest_framework import exceptions
from rest_framework import permissions

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
    message = "Unable to verify your location."

    def has_permission(self, request, view):
        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.can_bypass_location_check'):
            logger.info(
                'User: %s has bypassed the location check via permissions.' % request.user.username)
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
    message = "You must verify your identity to perform this action."

    def has_permission(self, request, view):
        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.can_bypass_identity_verification'):
            logger.info(
                'User: %s has bypassed the identity check via permissions.' % request.user.username)
            return True

        # Check if their identity is verified.
        return request.user.information.has_verified_identity


class EmailConfirmed(permissions.BasePermission):
    """
    Has the user verified their identity with Trulioo? If they have there will be a
    user.identity model.
    """
    message = "You must confirm your email address before performing this action"

    def has_permission(self, request, view):
        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.email_confirmation'):
            logger.info(
                'User: %s has bypassed the email confirmation via permissions.' % request.user.username)
            return True

        # Check if their identity is verified.
        return request.user.information.is_confirmed
