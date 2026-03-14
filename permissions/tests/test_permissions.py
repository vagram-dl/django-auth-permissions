from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from permissions.models import User,Role

class PermissionsTests(APITestCase):
    def setUp(self):
        self.role_user = Role.objects.create(name="user")
        self.role_admin = Role.objects.create(name="admin")

        self.user = User.objects.create_user(
            email = "perm@test.com",
            password = "password123",
            first_name = "Perm",
            last_name = "User",
            role = self.role_user
        )

        self.role_admin = Role.objects.create(name="Admin")
        self.admin = User.objects.create_user(
            email = "admin@test.com",
            password = "password123",
            first_name = "Admin",
            last_name = "User",
            role = self.role_admin,
            is_staff = True,
            is_superuser = True
        )
        self.url = reverse("access-rules-list")

    def test_request_without_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_request_with_user_role_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_request_with_admin_role_success(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)