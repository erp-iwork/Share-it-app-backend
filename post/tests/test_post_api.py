from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_NEW_POST = reverse("post:add_post")
GET_SINGLE_POST = reverse("post:post")


class PublicTestPostAPI(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_add_new_post(self):
        """Test to check adding new valid post is successfull"""
        payload = {"title": "title"}
        pass

    def test_add_new_post_with_empty_body(self):
        """Test to check sending empty body raises validation error"""
        payload = {}
        res = self.client.post(CREATE_NEW_POST, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("title", res.data)

    def test_add_new_post_with_no_image(self):
        """Test adding new post with no image fails"""
        payload = {}
        res = self.client.post(CREATE_NEW_POST, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_new_post_with_invalid_file_type(self):
        """Test adding new post with invalid file type fails"""
        payload = {}
        res = self.client.post(CREATE_NEW_POST, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_post_success(self):
        """Test update post is successful"""
        payload = {"title": "sometitle"}
        res.self.client.put(GET_SINGLE_POST, payload)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload.title, res.data)
