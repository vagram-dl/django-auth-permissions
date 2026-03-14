from django.contrib.admin.templatetags.admin_list import change_list_object_tools_tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from permissions.models import User,Role,AccessRoleRule, BusinessElement

class AccessRulesTests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(name="Admin")
        self.admin = User.objects.create_user(
            email = "admin@test.com",
            password = "password123",
            first_name = "Admin",
            last_name = "User",
            role = self.role_admin,
            is_staff = False,
            is_superuser = True
        )
        self.client.force_authenticate(user=self.admin)
        self.element = BusinessElement.objects.create(name="Dashboard")

        self.rule = AccessRoleRule.objects.create(
            role = self.role_admin,
            element = self.element,
            read_permission = True,
            create_permission = True,
            update_permission = True,
            delete_permission = True
        )

    def test_create_rule(self):
        url = reverse("access-rules-list")
        response = self.client.post(url,{
            "role" : self.role_admin.id,
            "element" : self.element.id,
            "read_permission" : True,
            "update_permission" : False,
            "delete_permission" : False
        })
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_list_rules(self):
        url = reverse("access-rules-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_rule(self):
        new_element = BusinessElement.objects.create(name="Dashboard Updated")
        url = reverse("access-rules-detail", args=[self.rule.id])
        response = self.client.put(url,{
            "role" : self.role_admin.id,
            "element" : new_element.id,
            "read_permission" : True,
            "create_permission" : True,
            "update_permission" : True,
            "delete_permission" : True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_rule(self):
        url = reverse("access-rules-detail", args=[self.rule.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
