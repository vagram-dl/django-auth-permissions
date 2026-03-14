from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from permissions.models import User, Role

class ProfileTests(APITestCase):
    def setUp(self):
        self.user_role = Role.objects.create(name="User")
        self.user = User.objects.create_user(
            email = "profile@test.com",
            password = "user123",
            first_name = "Test",
            last_name = "User",
            role = self.user_role,
            is_active = True
        )
        self.client.force_authenticate(user=self.user)

    def test_update_profile_success(self):
        url = reverse("update_user")
        data = {"first_name" : "Updated"}
        response = self.client.patch(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name,"Updated")

    def test_update_profile_without_auth(self):
        self.client.logout()
        url = reverse("update_user")
        data = {"first_name" : "NoAuth"}
        response = self.client.patch(url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_deleted_user(self):
        self.user.is_active = False
        self.user.save()
        url = reverse("update_user")
        data = {"first_name" : "Deleted"}
        response = self.client.patch(url,data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


