from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from django.conf import settings
import jwt

from permissions.models import User,JWT
from .serializers import LoginSerializer

class AuthService:
    @staticmethod
    def login_user(data):
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if user is None or not user.is_active:
            raise ValueError("Invalid credentials")

        payload = {"user_id" : user.id}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        expire_at = timezone.now() + timedelta(hours=1)
        JWT.objects.create(user=user, token=token, expire_at=expire_at)

        return {
            "token" : token,
            "email" : user.email,
            "expire_at" : expire_at
        }

    @staticmethod
    def logout_user(user):
        JWT.objects.filter(user=user).delete()
        return {"message" : "Logged out successfully"}