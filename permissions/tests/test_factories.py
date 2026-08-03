from django.test import TestCase
from permissions.factories import UserFactory
from permissions.models import User,Role

class UserFactoryTests(TestCase):
    def test_create_user(self):
        user = UserFactory.create_user(
            email = "factory_test@example.com",
            password = "super_secret_password",
            role_name = "Admin",
            first_name  = "Factory",
            last_name = "Test"
        )

        self.assertTrue(User.objects.filter(email = "factory_test@example.com").exists())
        self.assertNotEqual(user.password,"super_secret_password")
        self.assertTrue(user.check_password("super_secret_password"))
        self.assertEqual(user.role.name,"Admin")