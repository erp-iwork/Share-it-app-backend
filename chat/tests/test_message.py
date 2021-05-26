
from rest_framework import status
from rest_framework.test import APITestCase
from chat.models import Message
from main.models import  User

class MessageTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        response = Message.objects.create(
            sender="admin@gmail.com",
            receiver="endalk",
            message="Hey, This is the test message",
        )
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, message)