import jwt
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from permissions.models import JWT, User

class JWTAuthenticationMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                jwt_record = JWT.objects.filter(token=token).first()
                if not jwt_record:
                    return JsonResponse({"error" : "Invalid token"},status=401)
                if jwt_record.expire_at < timezone.now():
                    return JsonResponse({"error" : "Token expired"}, status=401)

                payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
                user_id = payload.get("user_id")
                request.user = User.objects.get(id=user_id)
            except Exception:
                return JsonResponse({"error" : "Unauthorized"},status=401)
        return self.get_response(request)

