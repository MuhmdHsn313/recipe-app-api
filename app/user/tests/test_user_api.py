from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREAT_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public user api."""

    def setUp(self):
        self.client = APIClient()

    def test_create_valide_user_success(self):
        """Test create a new valide user successful."""
        payload = {
            'email': 'user@test.com',
            'password': '1234abcd',
            'name': 'Test name'
        }

        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test creating user that already exists fails."""
        payload = {
            'email': 'user@test.com',
            'password': '1234abcd',
            'name': 'Test name'
        }
        create_user(**payload)

        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be than more 5 char."""
        payload = {
            'email': 'user@test.com',
            'password': '12',
            'name': 'Test name'
        }

        res = self.client.post(CREAT_USER_URL, **payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test creating a token for user when login."""
        payload = {
            'email': 'user@test.com',
            'password': '1234abcd',
            'name': 'Test name'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalide_credentials(self):
        "Test if that token is not created if invlide credentials are given."
        create_user(email='user@test.com', password='12345678')
        payload = {
            'email': 'user@test.com',
            'password': '1234abcd',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that no token created when no user exists."""
        payload = {
            'email': 'user@test.com',
            'password': '1234abcd',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required."""
        payload = {
            'email': 'user@test.com',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
