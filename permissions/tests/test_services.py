from django.test import TestCase
from unittest.mock import patch
from permissions.services import AuthService
from permissions.models import User,Role

class AuthServiceTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="User")
        self.user = User.objects.create_user(
            email = "mock@test.com",
            password = "testpass123",
            role = self.role
        )

    @patch('permissions.services.TokenRepository.save')
    def test_login_user_calls_repository_save(self,mock_save):
        login_data = {
            "email" : "mock@test.com",
            "password" : "testpass123"
        }

        result = AuthService.login_user(login_data)
        mock_save.assert_called_once()
        call_args = mock_save.call_args[0]
        self.assertEqual(call_args[0],self.user)
        self.assertIsInstance(call_args[1],str)
        self.assertIsNotNone(call_args[2])
        self.assertIn("token",result)
        self.assertEqual(result["email"],self.user.email)