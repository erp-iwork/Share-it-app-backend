from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
import os

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:signup")
LOGIN_USER = reverse("user:login")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    """Test the users API (user registeration and login)"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@gmail.com", password="user", name="user",
        )

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test@gmail.com",
            "password": "password",
            "name": "user",
            "location": "somewhere",
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
        payload = {
            "email": "test@gmail.com",
            "password": "112",
        }  # Check test works correctly
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"])

        self.assertFalse(user_exists)

    def test_updating_user_info(self):
        """Test updating user profile info"""
        GET_USER = reverse("user:get_user", args=[self.user.id])
        payload = {
            "email": "testing@gmail.com",
            "password": "password",
            "name": "updated user",
            "gender": "male",
        }

        res = self.client.put(GET_USER, payload)
        print(res)
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, "updated user")

    def test_deleting_user_info(self):
        """Test User account Deletion"""
        GET_USER = reverse("user:get_user", args=[self.user.id])
        res = self.client.delete(GET_USER)
        print(res)
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_login_success(self):
        """Test user login is successfull"""
        payload = {"email": "user@gmail.com", "password": "user"}
        res = self.client.post(LOGIN_USER, payload)
        print(res)
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, "token")

    def test_login_with_invalid_email(self):
        """Testing the user with not registered email address"""
        payload = {"email": "unregisterd@gmail.com", "password": "user"}
        res = self.client.post(LOGIN_USER, payload)
        print(res)
        print(res.data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_getting_authenticated_user(self):
        """Test that authentication is required for users"""
        GET_AUTH_USER = reverse("user:auth_user")
        res = self.client.get(GET_AUTH_USER)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    # def test_default_profile_image_is_uploaded(self):
    #     """Test the default profile image is set for user"""
    #     payload = {
    #         "email": "testimage@gmail.com",
    #         "password": "password",
    #         "name": "user",
    #         "location": "somewhere",
    #     }

    #     res = self.client.post(CREATE_USER_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertIn("image", res.data)
