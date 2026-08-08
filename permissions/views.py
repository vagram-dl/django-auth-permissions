import logging

logger = logging.getLogger(__name__)

from .services import AuthService
from .permissions import IsAdminRole
from rest_framework.throttling import ScopedRateThrottle
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
import jwt
from django.conf import settings

from permissions.models import User, AccessRoleRule, JWT
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, AccessRoleRuleSerializer
from rest_framework import viewsets, permissions




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []


class LoginThrottle(ScopedRateThrottle):
    scope = 'login'


class LoginView(APIView):
    throttle_classes = [LoginThrottle]
    throttle_scope = 'login'
    permission_classes = []

    def post(self,request):
        username = request.data.get('username')
        logger.info(f"Попытка входа пользователя: {username}")
        try:
            result = AuthService.login_user(request.data)
            logger.info(f"Успешный вход пользователя: {username}")
            return Response(result,status=status.HTTP_200_OK)
        except ValueError as e:
            client_ip = request.META.get('REMOTE_ADDR')
            logger.warning(f"Неудачная попытка входа для '{username}' с IP: {client_ip}")
            return Response({"error":str(e)},status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user.is_active:
            raise PermissionDenied("User is deactivated")
        return user

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message" : "User deactivated"} , status = status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        result = AuthService.logout_user(request.user)
        return Response(result,status=status.HTTP_200_OK)

class AccessRuleView(APIView):
    permission_classes = [IsAdminRole]

    def get(self,request):
        rules = AccessRoleRule.objects.select_related('role','element').all()
        data = [{
            "role" : r.role.name,
            "element" : r.element.name,
            "read" : r.read_permission,
            "create" : r.create_permission,
            "update" : r.update_permission,
            "delete" : r.delete_permission
        } for r in rules]
        return JsonResponse(data,safe=False)

def get_users_json(queryset):
    data = [
        {
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email
        }
        for u in queryset
    ]
    return JsonResponse(data,safe=False)

def active_users(request):
    users = User.objects.filter(role__name = "User",is_active = True)
    return get_users_json(users)


def admin_users(request):
    admins = User.objects.filter(role__name="Admin", is_active=True)
    return get_users_json(admins)

def example_users(request):
    users = User.objects.filter(email__endswith="@example.com")
    return get_users_json(users)

def recent_users(request):
    users = User.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))
    return get_users_json(users)


def managers_or_users(request):
    users = User.objects.filter(Q(role__name="Manager") | Q(role__name="User"))
    return get_users_json(users)

def user_access_rules(request):
    rules = AccessRoleRule.objects.select_related('role','element').filter(
        role__name = "User",
        element__name = "Orders",
        read_permission = True
    )
    data = [{
        "role":r.role.name,
        "element": r.element.name,
        "can_read": r.read_permission
    }for r in rules]
    return JsonResponse(data, safe=False)





class AccessRoleRuleViewSet(viewsets.ModelViewSet):
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
       return AccessRoleRule.objects.select_related('role','element').all()


    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


# Create your views here.
