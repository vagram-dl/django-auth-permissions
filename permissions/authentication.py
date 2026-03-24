import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions
from permissions.models import JWT,User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]

        try:
            jwt_record = JWT.objects.filter(token=token).first()
            if not jwt_record:
                raise exceptions.AuthenticationFailed("Invalid token")

            if jwt_record.expire_at < timezone.now():
                raise exceptions.AuthenticationFailed("Token expired")
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
            return (user,token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
        except Exception:
            raise exceptions.AuthenticationFailed("Unauthorized")

    def authenticate_header(self, request):
        return 'Bearer realm="api"'