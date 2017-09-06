import calendar
import logging
from datetime import datetime, date, timedelta

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authLogin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from rest_framework import generics
from rest_framework import response, schemas
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import (ValidationError)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

import account.tasks
from account.forms import (
    LoginForm,
    SelfExclusionForm,
)
from account.gidx.models import GidxSession
from account.gidx.request import (
    CustomerRegistrationRequest,
    WebRegCreateSession,
    WebCashierCreateSession,
    RegistrationStatusRequest,
    get_user_from_session_id,
    get_customer_id_for_user,
    make_web_cashier_payment_detail_request,
)
from account.gidx.response import (
    IdentityStatusWebhookResponse,
    GidxTransactionStatusWebhookResponse
)
from account.models import Identity
from account.models import (
    Information,
    EmailNotification,
    UserEmailNotification,
    Limit
)
from account.permissions import (
    HasIpAccess,
    HasVerifiedIdentity,
)
from account.serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    RegisterUserSerializer,
    UserSerializer,
    UserCredentialsSerializer,
    UserSerializerNoPassword,
    UserEmailNotificationSerializer,
    UpdateUserEmailNotificationSerializer,
    UserLimitsSerializer,
    VerifyUserIdentitySerializer
)
from account.utils import (get_client_ip)
from account.utils import send_welcome_email
from contest.models import CurrentEntry
from contest.refund.tasks import unregister_entry_task

logger = logging.getLogger('account.views')


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    """
    Swagger documentation
    """
    generator = schemas.SchemaGenerator(title='Draftboard API')
    return response.Response(generator.get_schema(request=request))


class AuthAPIView(APIView):
    """
    Login endpoint. POST to login. DELETE to logout.
    """

    authentication_classes = (BasicAuthentication,)
    serializer_class = LoginSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        args = request.data
        user = authenticate(username=args.get('username'),
                            password=args.get('password'))
        if user is not None:
            authLogin(request, user)
            #
            # return a 201
            return Response({}, status=status.HTTP_200_OK)

        #
        # the case they dont login properly
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def delete(request, *args, **kwargs):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    """
    This api always return http 200.

    If the specified email is actually associated with a user,
    issue an email, and generate a temp password hash for them.
    """

    authentication_classes = (BasicAuthentication,)
    serializer_class = ForgotPasswordSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        #
        # validate this email is associated with a user in the db,
        # and if it is, send a password reset email to that account.
        args = request.data
        email = args.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None  # no user found... moving on.

            if user:
                #
                # fire the task that sends a password reset email to this user
                account.tasks.send_password_reset_email.delay(user)

                #
                #
        #
        # return success no matter what
        return Response({}, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    # handles
    # https://www.draftboard.com/api/account/password-reset-confirm/MjA0/47k-95ee193717cb75448cf0/
    authentication_classes = (BasicAuthentication,)
    serializer_class = PasswordResetSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        args = request.data
        uid = args.get('uid')
        token = args.get('token')

        if uid and token:
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class UserAPIView(generics.RetrieveAPIView):
    """
    General user information.

    * |api-text| :dfs:`account/user/`
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserCredentialsAPIView(generics.GenericAPIView):
    """
    Allows the logged in user to modify their password and email.

        .. note::

            If username is modified in the put, it will not be saved.

        * |api-text| :dfs:`account/settings/`
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserCredentialsSerializer

    def get_object(self):
        user = self.request.user
        return user

    def post(self, request):
        user = self.get_object()
        data = request.data
        serializer = self.serializer_class(user, data=data, partial=True)

        if serializer.is_valid():
            if data.get('email'):
                user.email = data.get('email')
            if data.get('password'):
                user.set_password(data.get('password'))
            user.save()
            return Response(UserSerializerNoPassword(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailNotificationAPIView(generics.GenericAPIView):
    """
    Allows the user to get and update their user email settings

        * |api-text| :dfs:`account/notifications/email/`
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserEmailNotificationSerializer

    # Get all of the notification types, then run through each type and check if the user has a
    # setting, if not, create one in get_object().
    def get_objects(self):
        user = self.request.user
        notifications = EmailNotification.objects.filter(deprecated=False)
        for notif in notifications:
            self.get_object(notif)

        return UserEmailNotification.objects.filter(user=user)

    def get_object(self, notif):
        user = self.request.user

        try:
            email_notif = UserEmailNotification.objects.get(
                user=user,
                email_notification=notif
            )
        except UserEmailNotification.DoesNotExist:
            #
            # Creates the corresponding email notification
            email_notif = UserEmailNotification()
            email_notif.email_notification = notif
            email_notif.user = user
            email_notif.save()

        return email_notif

    def get(self, request):
        user_email_notifications = self.get_objects()
        serializer = UserEmailNotificationSerializer(user_email_notifications, many=True)

        return Response(serializer.data)

    # Update a list of UserEmailNotifications.
    def post(self, request):
        errors = []

        # Run through each supplied UserEmailNotification, updating the 'enabled' field and saving.
        for setting in request.data:
            try:
                notif = EmailNotification.objects.get(
                    deprecated=False,
                    id=setting['id']
                )
            except EmailNotification.DoesNotExist:
                errors.append("Notification id: %s does not exist" % setting.id)

            # Get the UserEmailNotification from the DB, and update the enabled field.
            user_email_notification = self.get_object(notif)
            user_email_notification.enabled = setting['enabled']
            serializer = UpdateUserEmailNotificationSerializer(
                user_email_notification, data=setting, many=False
            )
            # Save or add error to errors list.
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request)


def login(request, **kwargs):
    """
    Extension of the Django login view, redirects to the feed if already logged in.
    Unfortunately Django does not use class based views for auth so we must keep this old as well.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frontend:lobby'))

    return auth_views.login(request, authentication_form=LoginForm)


class RegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        """
        if already logged in, redirect to lobby, otherwise allow page
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('frontend:lobby'))

        return super(RegisterView, self).get(request, *args, **kwargs)

    template_name = 'registration/register.html'


class VerifyLocationAPIView(APIView):
    """
    A simple endpoint to run the HasIpAccess permission class.
    If the user's IP acceptable, return 200. otherwise a 403.
    This location check is done with our local IP database. This does NOT
    use GIDX to do a hard check on the user.
    """
    permission_classes = (HasIpAccess,)

    @staticmethod
    def get(request):
        return Response(
            data={
                "status": "SUCCESS",
                "detail": "location verification passed"
            },
            status=200,
        )


class GidxRegistrationStatus(APIView):
    """
    Check the status of a user registration session. This is used after the drop-in form is
    complete and we need to check for a pass/fail.
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, merchant_session_id):
        status_request = RegistrationStatusRequest(
            user=request.user,
            merchant_session_id=merchant_session_id
        )

        # Verify data and send!
        status_response = status_request.send()

        # If the user was verified...
        if status_response.is_verified():
            # If GIDX says they are verified, we save some of the identity info.
            # Note: we don't get a DOB back from the webhook, so we can't add one.
            # I'm not totally sure what the ramifications of that may be.

            # Since they may already have an Identity for some reason, try to get it
            # first, if not, create a new one.
            identity, created = Identity.objects.get_or_create(user=request.user)

            identity.gidx_customer_id = get_customer_id_for_user(request.user)
            identity.flagged = status_response.is_identity_previously_claimed()
            identity.metadata = status_response.json
            identity.country = status_response.get_country()
            identity.region = status_response.get_region()
            identity.status = True
            identity.save()

            return Response(
                data={
                    "status": "SUCCESS",
                    "detail": "Your Identity has been verified!"
                },
                status=200,
            )

        return Response(
            data={
                "status": "FAIL",
                "detail": "Your Identity could not be verified"
            },
            status=200,
        )


class GidxIdentityCallbackAPIView(APIView):
    """
    When a user can't be validated via direct API, we use the GIDX drop-in form
    and attempt to verify that way. When that form is submitted, GIDX sends a callback webhook
    with the status to our server.
    """

    parser_classes = (MultiPartParser, FormParser,)

    @staticmethod
    @csrf_exempt
    def post(request):
        import json

        request_data = json.loads(request.data.dict()['result'])

        logger.info({
            "action": "WebReg_Callback",
            "request": None,
            "response": request_data,
        })

        response_wrapper = IdentityStatusWebhookResponse(request_data)
        # Grab some of the data from the previous session that is not included in the webhook.
        user = get_user_from_session_id(response_wrapper.json['MerchantSessionID'])
        customer_id = get_customer_id_for_user(user)

        # Save our session info
        GidxSession.objects.create(
            user=user,
            gidx_customer_id=customer_id,
            session_id=response_wrapper.json['MerchantSessionID'],
            service_type='WebReg_Callback',
            reason_codes=response_wrapper.json['ReasonCodes'],
            response_data=request_data,

        )

        if response_wrapper.is_verified():
            # If GIDX says they are verified, we save some of the identity info.
            # Note: we don't get a DOB back from the webhook, so we can't add one.
            # I'm not totally sure what the ramifications of that may be.

            # Since they may already have an Identity for some reason, try to get it
            # first, if not, create a new one.
            identity, created = Identity.objects.get_or_create(user=user)

            identity.gidx_customer_id = customer_id
            identity.country = response_wrapper.get_country()
            identity.region = response_wrapper.get_region()
            identity.flagged = response_wrapper.is_identity_previously_claimed()
            identity.metadata = request_data
            identity.status = True
            identity.save()

        return Response(
            data={
                # "CustomerID": customer_id,
                # "MerchantID": settings.GIDX_MERCHANT_ID,
                # "SessionStatus": response_wrapper.json['StatusCode'],
                "status": "SUCCESS",
                "detail": "cool, thanks!"
            },
            status=200,
        )


class VerifyUserIdentityAPIView(APIView):
    """
    Uses GIDX to verify the user's identity. If the GIDX request was a success, we set the
    user's account as 'verified'.
    If this fails, the client will proceed to the advanced GIDX-provided JS drop-in form.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VerifyUserIdentitySerializer

    def post(self, request):
        # First, check if they already have a verified identity.
        if request.user.information.has_verified_identity:
            logger.warning(
                'Previously verified user is attempting to verify their identity. %s' % (
                    request.user))
            return Response(
                data={
                    "status": "SUCCESS",
                    "detail": "User already has a verified identity"
                },
                status=200,
            )

        # If not. validate the input data.
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Prepare a request to the GIDX API.
            crr = CustomerRegistrationRequest(
                user=request.user,
                first_name=serializer.validated_data.get('first'),
                last_name=serializer.validated_data.get('last'),
                date_of_birth="%02d/%02d/%s" % (
                    serializer.validated_data.get('birth_month'),
                    serializer.validated_data.get('birth_day'),
                    serializer.validated_data.get('birth_year'),
                ),
                ip_address=get_client_ip(request)
            )
            # Verify data and send!
            registration_response = crr.send()

            # If the user was verified...
            if registration_response.is_verified():
                # If  the identity has already been claimed, bail out of here, don't validate,
                # return an error.
                if registration_response.is_identity_previously_claimed():
                    return Response(
                        data={
                            "status": "FAIL_FINAL",
                            "detail": "We are terribly sorry but we are unable to verify your "
                                      "account through our automated service. Please contact "
                                      "support@draftboard.com and we’ll get you activated as "
                                      "soon as possible.",
                            "reasonCodes": registration_response.get_reason_codes(),
                        },
                        status=400,
                    )

                # create a date out of the input.
                dob = datetime(
                    serializer.validated_data.get('birth_year'),
                    serializer.validated_data.get('birth_month'),
                    serializer.validated_data.get('birth_day')
                )
                # If GIDX says they are verified, we save the some of the identity info.
                # Since they may already have an Identity for some reason, try to get it
                # first, if not, create a new one.
                identity, created = Identity.objects.get_or_create(user=request.user)
                identity.dob = dob
                identity.gidx_customer_id = registration_response.json['MerchantCustomerID']
                identity.country = registration_response.get_country()
                identity.region = registration_response.get_region()
                identity.flagged = registration_response.is_identity_previously_claimed()
                identity.metadata = registration_response.json
                identity.status = True
                identity.save()

                return Response(
                    data={
                        "status": "SUCCESS",
                        "detail": "Your identity has been verified."
                    },
                    status=200,
                )

            # If not verified, get a JS snippet to embed the advanced form.
            web_reg = WebRegCreateSession(
                user=request.user,
                first_name=serializer.validated_data.get('first'),
                last_name=serializer.validated_data.get('last'),
                date_of_birth="%02d/%02d/%s" % (
                    serializer.validated_data.get('birth_month'),
                    serializer.validated_data.get('birth_day'),
                    serializer.validated_data.get('birth_year'),
                ),
                ip_address=get_client_ip(request)
            )
            # Make the request.
            web_reg_response = web_reg.send()

            # If we requested a JS embed, and GIDX says they are already verified, go ahead and
            # update the user's identity.
            if web_reg_response.is_verified():
                identity, created = Identity.objects.get_or_create(user=request.user)
                identity.metadata = web_reg_response.json
                identity.flagged = web_reg_response.is_identity_previously_claimed()
                identity.status = True
                identity.save()

                return Response(
                    data={
                        "status": "SUCCESS",
                        "detail": "Your identity has been verified."
                    },
                    status=200,
                )

            message = web_reg_response.get_response_message()
            if not message:
                message = "We were unable to verify your identity."

            return Response(
                data={
                    "status": "FAIL",
                    "detail": message,
                    "reasonCodes": registration_response.get_reason_codes(),
                },
                status=400,
            )


class GidxDepositAPIView(APIView):
    """
    Begin process of depositing to the site using the gidx WebCashier service.
    If everything goes fine, gidx will return to us an embeddable javascript form.
    """
    permission_classes = (IsAuthenticated, HasVerifiedIdentity, HasIpAccess)

    def get(self, request, *args, **kwargs):
        web_cashier = WebCashierCreateSession(
            ip_address=get_client_ip(request),
            user=request.user,
        )
        # Make the request.
        web_cashier_response = web_cashier.send()
        message = web_cashier_response.get_response_message()

        # If we didn't receive a JS embed...
        if not message:
            return Response(
                data={
                    "status": "FAIL",
                    "detail": "We were unable to initiate the withdraw process.",
                    "reasonCodes": web_cashier_response.get_reason_codes(),
                },
                status=400,
            )

        return Response(
            data={
                "status": "SUCCESS",
                "detail": message,
                "reasonCodes": web_cashier_response.get_reason_codes(),
            },
            status=200,
        )


class GidxDepositCallbackAPIView(APIView):
    """
    Note: this very similar to GidxWithdrawCallbackAPIView -- maybe these can be merged?

    When a user deposits money, we embed a gidx-provided form. When the form is submitted and
    the transaction processed, we will get a request to this endpoint with info about
    the transaction.
    """

    parser_classes = (MultiPartParser, FormParser,)

    @staticmethod
    @csrf_exempt
    def post(request):
        import json

        request_data = json.loads(request.data.dict()['result'])

        logger.info({
            "action": "WebCashier_Deposit_Callback",
            "request": None,
            "response": request_data,
        })

        response_wrapper = GidxTransactionStatusWebhookResponse(request_data)
        # Grab some of the data from the previous session that is not included in the webhook.
        user = get_user_from_session_id(response_wrapper.json['MerchantSessionID'])
        customer_id = get_customer_id_for_user(user)

        # Save our session info
        GidxSession.objects.create(
            user=user,
            gidx_customer_id=customer_id,
            session_id=response_wrapper.json['MerchantSessionID'],
            service_type='WebCashier_Deposit_Callback',
            reason_codes=response_wrapper.json['ReasonCodes'],
            response_data=request_data,
        )

        # If the webhook says that the transaction has completed (good or bad), we need to fetch
        # the payment details in order to proceed.

        if response_wrapper.is_done():
            payment_detail = make_web_cashier_payment_detail_request.delay(
                user=user,
                transaction_id=response_wrapper.json['MerchantTransactionID'],
                session_id=response_wrapper.json['MerchantSessionID']
            )
        else:
            logger.warning('Transaction pending or failed: %s' % response_wrapper.json)

        # As long as nothing errors out, send a 200 back to gidx.
        return Response(
            data={
                "status": "SUCCESS",
                "detail": "cool, thanks!"
            },
            status=200,
        )


class RegisterAccountAPIView(APIView):
    """
    Create a user account, Information object, and log the user in.

    example POST param (JSON):

    {"username": "myUserName", "password": "pa$$word", "email": "me@email.com"}
    """

    permission_classes = ()
    register_user_serializer_class = RegisterUserSerializer

    def post(self, request):
        # - Attempt to create User account.
        user_serializer = self.register_user_serializer_class(data=request.data)

        if user_serializer.is_valid(raise_exception=True):
            username = user_serializer.validated_data.get('username')
            email = user_serializer.validated_data.get('email')
            password = user_serializer.validated_data.get('password')

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            # Make sure each user gets an information model.
            Information.objects.create(user=user)
            new_user = authenticate(username=user.username, password=password)

            # Log user in.
            if new_user is not None:
                authLogin(request, new_user)

            # Send a welcome email.
            send_welcome_email(new_user)

            # Everything went OK!
            return Response(data={"detail": "Account Created"}, status=status.HTTP_201_CREATED)

        # If there were user user_serializer errors, send em back to the user.
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessSubdomainsTemplateView(LoginRequiredMixin, TemplateView):
    """
    A view that, if you have access, sets a cookie to let you view other Run It Once sites in development.
    """
    template_name = 'frontend/access_subdomains.html'

    def render_to_response(self, context, **response_kwargs):
        """
        If user is logged in, redirect them to their feed
        """
        response = super(AccessSubdomainsTemplateView, self).render_to_response(context,
                                                                                **response_kwargs)

        if not self.request.user.has_perm('auth.access_subdomains'):
            raise Http404

        days_expire = 7
        max_age = days_expire * 24 * 60 * 60
        expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),
                                    "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie('access_subdomains', 'true', max_age=max_age, expires=expires,
                            domain=settings.COOKIE_ACCESS_DOMAIN)
        return response


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


class ExclusionFormView(FormView):
    template_name = 'frontend/self-exclusion.html'
    form_class = SelfExclusionForm
    success_url = '/'
    months = [3, 6, 9, 12]

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data()
        cur_date = date.today()
        for month in self.months:
            kwargs['%s_month' % month] = add_months(cur_date, month)
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.information
        return kwargs

    def form_valid(self, form):
        information = form.save()
        entries = CurrentEntry.objects.filter(user=information.user)
        for entry in entries:
            unregister_entry_task.delay(entry)
            UserEmailNotification.objects.filter(user=information.user).update(enabled=False)
            logout(self.request)
        return super().form_valid(form)


class UserLimitsAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = UserLimitsSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        limits = user.limits.all()
        user_limits = []
        serializer = None
        if limits.exists():
            serializer = self.serializer_class(limits, many=True)
        else:
            for limit_type in Limit.TYPES:
                limit_type_index = limit_type[0]
                val = Limit.TYPES_GLOBAL[limit_type_index]['value'][0][0]
                user_limits.append({'user': user.pk,
                                    'type': limit_type_index,
                                    'value': val,
                                    'time_period': Limit.PERIODS[0][
                                        0] if limit_type != Limit.ENTRY_FEE else None})
        limits_data = {'types': Limit.TYPES_GLOBAL,
                       'current_values': serializer.data if serializer else user_limits}
        return Response(limits_data)

    def post(self, request, *args, **kwargs):
        user = request.user
        limits = user.limits.all()

        if limits.exists():
            serializer = self.serializer_class(limits, data=self.request.data, many=True)
            # If the user has no Identity, we can't set play limits.
            if not user.information.has_verified_identity:
                raise ValidationError(
                    {'detail': 'You must verify your identity before setting play limits.'})
            state = user.identity.state
            if state:
                days = settings.LIMIT_DAYS_RESTRAINT.get(state)
                if days:
                    change_allowed_on = limits[0].updated + timedelta(days=days)
                    if timezone.now() < change_allowed_on:
                        return JsonResponse(data={
                            "detail": "Not allowed to change limits until {}".format(
                                change_allowed_on.strftime('%Y-%m-%d %I:%M %p'))}, status=400,
                            safe=False)

        else:
            serializer = self.serializer_class(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"detail": "Limits Saved"}, status=200)
