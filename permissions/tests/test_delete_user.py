from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from permissions.models import User,Role

class DeleteUserTests(APITestCase):
    def setUp(self):
        role = Role.objects.create(name="user")
        self.user = User.objects.create_user(
            email = "delete@test.com",
            password = "password123",
            first_name = "Delete",
            last_name = "User",
            role = role
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("delete_user")

    def test_delete_user_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_login_after_deletion(self):
        self.client.delete(self.url)
        login_url = reverse("login")
        response = self.client.post(login_url,{
            "email" : "delete@test.com",
            "password" : "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

