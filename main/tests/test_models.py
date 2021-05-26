from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_success(self):
        """Test creating a new user with email is successful"""
        email = "test@gmail.com"
        password = 1234567
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):
        """Test the email field is normalized"""
        email = "test@EXAMPLE.com"
        password = 1234567
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEquals(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """"Test creating user with invalid email raises error"""
        with self.assertRaises(ValueError):
            password = 1234567
            user = get_user_model().objects.create_user(None, password=password)

    def test_create_new_superuser(self):
        """Test Creating a new super user """
        email = "superuser@gmail.com"
        password = 1234567
        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
