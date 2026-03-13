from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from permissions.models import Role, AccessRoleRule, BusinessElement

User = get_user_model()

class AccessRoleCRUDTests(APITestCase):
    def setUp(self):
        self.admin_role = Role.objects.create(name="Admin")
        self.user_role = Role.objects.create(name="User")
        self.element = BusinessElement.objects.create(name="Users")

        self.admin = User.objects.create_user(
            email = "admin@test.com", password = "user123", role = self.admin_role
        )

        self.user = User.objects.create_user(
            email = "user@test.com", password = "user123", role = self.user_role
        )

        self.rule = AccessRoleRule.objects.create(
            role = self.admin_role,
            element = self.element,
            read_permission = True,
            create_permission = True,
            update_permission = True,
            delete_permission = True
        )
    def test_admin_can_create_rule(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/access-rules/",{
            "role" : self.admin_role.id,
            "element" : self.element.id,
            "read_permission" : True,
            "create_permission" : True,
            "update_permission" : True,
            "delete_permission" : True
        })
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_user_cannot_create_rule(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/access-rules/",{
            "role" : self.user_role.id,
            "element" : self.element.id,
            "read_permission" : True,
            "create_permission" : False,
            "update_permission" : False,
            "delete_permission" : False
        })
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
