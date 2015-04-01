
import unittest
import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
class RegisterAccountTest( APITestCase ):

    def test_api(self):
        invalid_password_data = {'username': 'user',
                                 'email': 'user@test.com',
                                 'password': '',
                                 }
        missing_password_data = {'username': 'user',
                                 'email': "user@test.com",
                                 }
        invalid_username_data = {'username': '',
                                 'email': "user@test.com",
                                 'password': 'password',
                                 }
        missing_username_data = {'email': "user@test.com",
                                 'password': 'password',
                                }
        invalid_email_data = {'username': 'user',
                              'email': "usertest.com",
                              'password': 'password',
                             }
        missing_email_data = {'username': 'user',
                              'password': 'password',
                             }
        proper_data = {'username': 'user',
                     'email': "user@test.com",
                     'password': 'password',
                     }


        url = '/account/register/'

        #
        # Tests for invalid password
        response = self.client.post(url, invalid_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST )

        #
        # Tests for missing password field
        response = self.client.post(url, missing_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for invalid username
        response = self.client.post(url, invalid_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for missing username field
        response = self.client.post(url, missing_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for invalid email data
        response = self.client.post(url, invalid_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for missing email data
        response = self.client.post(url, missing_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for proper creation
        response = self.client.post(url, proper_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #
        # Tests for duplicates
        response = self.client.post(url, proper_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



