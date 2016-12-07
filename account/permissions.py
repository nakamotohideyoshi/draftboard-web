from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import exceptions
from .utils import CheckUserAccess
import logging

logger = logging.getLogger('account.permissions')


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
    def has_permission(self, request, view):
        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.can_bypass_identity_verification'):
            logger.info(
                'User: %s has bypassed the identity check via permissions.' % request.user.username)
            return True

        # Check if their identity is verified.
        return request.user.information.has_verified_identity


class IsConfirmed(permissions.BasePermission):
    """
    Has the user verified their identity with Trulioo? If they have there will be a
    user.identity model.
    """
    def has_permission(self, request, view):
        # If the user has permission to bypass location checks, pass them.
        if request.user.has_perm('account.email_confirmation'):
            logger.info(
                'User: %s has bypassed the email confirmation via permissions.' % request.user.username)
            return True

        # Check if their identity is verified.
        return request.user.information.is_confirmed
