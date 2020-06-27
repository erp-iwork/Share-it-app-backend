from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        """Setup an admin user and a dummy use for test"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com", password="admin"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@gmail.com", password="user", name="user"
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse("admin:main_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:main_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_adding_user_model(self):
        """Test user creation page works"""
        url = reverse("admin:main_user_add")
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)
