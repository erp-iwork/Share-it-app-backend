from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    """Test the users API (user registeration and login)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test@gmail.com",
            "password": "password",
            "first_name": "user",
            "last_name": "test",
            "gender": "male",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_exists(self):
        """Testing a user already exists"""
        payload = {
            "email": "test@gmail.com",
            "password": "password",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short(self):
        """Test that the password must be more than 8 characters"""
        payload = {"email": "test@gmail.com", "password": "112"}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"])

        self.assertFalse(user_exists)

    def test_getting_user_lists(self):
        """Test all user lists"""

        res = self.client.get("CREATE_USER_URL")
        print(res.data)
        print(res.status_code)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
