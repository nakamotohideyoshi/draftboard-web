from django.test import TestCase
from rest_framework.test import APIClient
from model_mommy import mommy
from django.contrib.auth.models import User
from rest_framework.exceptions import (APIException, ValidationError)
from pprint import pprint
from account.models import Information
from django.contrib.auth import get_user_model
import responses
from ..request import (
    WebRegCreateSession,
)
from ..mock_response_data import (
    WEB_REG_SUCCESS_RESPONSE,
)
import json


class TestVerifyUserIdentityAPIView(TestCase):
    client = APIClient(enforce_csrf_checks=False)
    user = None

    def setUp(self):
        # Create a user.
        self.user = get_user_model().objects.create_user(
            username="automated_test_user",
            email="me@zacharywood.com",
            password='password'
        )
        # give them an Info model too.
        mommy.make(Information, user=self.user)
        # now log that user in.
        self.client.login(username=self.user.username, password='password')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    # I don't know why this doesn't work.
    # @responses.activate
    # def test_returns_script_tag(self):
    #     # Mock the API call that this view makes.
    #     responses.add(
    #         responses.POST,
    #         WebRegCreateSession.url,
    #         body=str(json.dumps(WEB_REG_SUCCESS_RESPONSE)),
    #         status=200,
    #         content_type='application/json'
    #     )
    #
    #     response = self.client.post('/api/account/verify-user/', {
    #         'first': 'test_first',
    #         'last': 'test_last',
    #         'birth_month': 2,
    #         'birth_day': 22,
    #         'birth_year': 1984
    #     })
    #
    #     pprint(response.content)
    #     self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_invalid_data(self):
        # missing first and last name.
        response = self.client.post('/api/account/verify-user/', {
            'first': '',
            'last': '',
            'birth_month': 2,
            'birth_day': 22,
            'birth_year': 1984
        })

        self.assertIn('last', response.data)
        self.assertIn('first', response.data)
        self.assertEqual(response.status_code, 400)
