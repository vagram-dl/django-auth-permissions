from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from permissions.models import User,Role

class AuthTests(APITestCase):
    def setUp(self):
        self.user_role = Role.objects.create(name="User")

        self.User = User.objects.create_user(
            email = "user@example.com",
            password = "user123",
            first_name = "Normal",
            last_name = "User",
            role = self.user_role,
            is_active = True
        )
    def test_register_user(self):
        url = reverse("register")
        data = {
            "email" : "new@example.com",
            "first_name" : "New",
            "last_name" : "User",
            "password" : "newpass123"
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_login_valid_user(self):
        url = reverse("login")
        data = {"email" : "user@example.com", "password":"user123"}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn("token",response.data)

    def test_login_invalid_user(self):
        url = reverse("login")
        data = {"email" : "user@example.com", "password" : "wrongpass"}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_profile_required_auth(self):
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)