from logging import getLogger

from raven.contrib.django.raven_compat.models import client
from rest_framework.exceptions import (APIException, ValidationError)

from account import const as _account_const
from account.models import Identity
from account.utils import create_user_log
from trulioo.classes import (
    Trulioo,
    VerifyDataValidationError,
    TruliooException
)

logger = getLogger('trulioo.utils')


def find_existing_identites(first, last, birth_day, birth_month, birth_year, postal_code):
    """
    Find any identites in our database that match the input.

    :param first:
    :param last:
    :param birth_day:
    :param birth_month:
    :param birth_year:
    :param postal_code:
    :return:
    """
    return Identity.objects.filter(
        first_name__iexact=first,
        last_name__iexact=last,
        birth_day=birth_day,
        birth_month=birth_month,
        birth_year=birth_year,
        postal_code=postal_code,
    ).exists()


def find_similar_identites(first, last, birth_day, birth_month, birth_year, postal_code):
    """
    Trulioo has some leeway when verifying identites. For instance it will match "dan" as
    "daniel". Or a user could enter an old postal code and it will verify. What we want to do
    is flag the users that have slightly different info from any identities we have already
    verified. When a flagged identity is created, a notification is sent to the site admin
    for manual investigation.

    :param first:
    :param last:
    :param birth_day:
    :param birth_month:
    :param birth_year:
    :param postal_code:
    :return:
    """
    return Identity.objects.filter(
        birth_day=birth_day,
        birth_month=birth_month,
        birth_year=birth_year,
        last_name__iexact=last,
    ).exists()


def verify_user_identity(first, last, birth_day, birth_month, birth_year, postal_code):
    # First check if we have an existing user match in our DB.
    # It is hiiighly unlikely that we'll have 2 users with the same
    # last name, DOB, & postal code. If we do, they can be manually added.
    existing_identities = find_existing_identites(
        first, last, birth_day, birth_month, birth_year, postal_code,
    )

    # If the identity is already claimed, log and return errror message.
    if existing_identities:
        logger.warning("IDENTITY_VERIFICATION_EXISTS")
        create_user_log(
            request=None,
            type=_account_const.AUTHENTICATION,
            action=_account_const.IDENTITY_VERIFICATION_EXISTS,
            metadata={'detail': """User attampted to claim an identity that already exists in
                        our database.""", }
        )
        raise ValidationError({
            "detail": "Unable to verify your identity. Please contact support@draftboard.com"})

    # use Trulioo class to verify the user
    try:
        t = Trulioo()
        verified = t.verify_minimal(
            first=first, last=last, birth_day=birth_day, birth_month=birth_month,
            birth_year=birth_year, postal_code=postal_code)

    # Send data validation exceptions back through the API.
    except VerifyDataValidationError as e:
        logger.warning("%s" % e)
        raise ValidationError({"detail": str(e)})

    # There was a data validation error sent back from Trulioo.
    except TruliooException as e:
        logger.warning("%s" % e)
        raise ValidationError({"detail": str(e)})

    # Log all others before sending the user a generic response.
    except Exception as e:
        logger.warning("%s" % e)
        client.captureException()
        raise APIException(
            'User verification was unsuccessful. Please contact support@draftboard.com')

    if verified is False:
        logger.warning('IDENTITY_VERIFICATION_FAILED - no match found.')
        # Create a user log for the failed attempt.
        create_user_log(
            request=None,
            type=_account_const.AUTHENTICATION,
            action=_account_const.IDENTITY_VERIFICATION_FAILED,
            metadata={
                'detail': 'No identity match was found for provided info.',
            }
        )

        raise ValidationError(
            'User verification was unsuccessful. Please contact support@draftboard.com')


def create_user_identity(user, first, last, birth_day, birth_month, birth_year, postal_code):
    """
    Save the information so that we can do multi-account checking.

    :param user:
    :param first:
    :param last:
    :param birth_day:
    :param birth_month:
    :param birth_year:
    :param postal_code:
    :return:
    """

    # Search for similar identities
    similar_identity_exists = find_similar_identites(
        first, last, birth_day, birth_month, birth_year, postal_code,
    )

    # Create the identity, flagging it if there is already a similar one in the database.
    identity = Identity(
        user=user, first_name=first, last_name=last, birth_day=birth_day,
        birth_month=birth_month, birth_year=birth_year, postal_code=postal_code,
        flagged=similar_identity_exists)
    identity.save()

    # Log out some warnings for alerting purposes.
    if similar_identity_exists:
        logger.warning("SIMILAR_IDENTITY_EXISTS - user: %s" % user)

    # Create a user log for the verification.
    logger.info("IDENTITY_VERIFICATION_SUCCESS - user: %s" % user)
    create_user_log(
        user=user,
        type=_account_const.AUTHENTICATION,
        action=_account_const.IDENTITY_VERIFICATION_SUCCESS,
        metadata={
            'detail': 'An identity match was found.',
            'UserIdentity.pk:': identity.pk,
        }
    )
