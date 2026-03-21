from rest_framework.throttling import ScopedRateThrottle
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
import jwt
from django.conf import settings

from permissions.models import User, AccessRoleRule,JWT
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
from rest_framework import viewsets, permissions
from permissions.models import AccessRoleRule
from .serializers import AccessRoleRuleSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginThrottle(ScopedRateThrottle):
    scope = 'login'


class LoginView(APIView):
    throttle_classes = [LoginThrottle]
    throttle_scope = 'login'

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request,email=email,password=password)
        if user is None or not user.is_active:
            return Response({"error":"Invalid credentials"},status.HTTP_401_UNAUTHORIZED)

        payload = {"user_id" : user.id}
        token = jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")

        expire_at = timezone.now() + timedelta(hours=1)
        JWT.objects.create(user=user, token=token, expire_at=expire_at)

        return Response({"token" : token, "email" : user.email,"expire_at" : expire_at})

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
        JWT.objects.filter(user=request.user).delete()
        return Response({"message" : "Logged out successfully"},status=status.HTTP_200_OK)

class AccessRuleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.user.role.name != "Admin":
            return Response({"error" : "Forbidden"}, status.HTTP_403_FORBIDDEN)
        rules = AccessRoleRule.objects.all()
        data = [{
            "role" : r.role.name,
            "element" : r.element.name,
            "read" : r.read_permission,
            "create" : r.create_permission,
            "update" : r.update_permission,
            "delete" : r.delete_permission
        } for r in rules]
        return JsonResponse(data,safe=False)

def active_users(request):
    users = User.objects.filter(role__name="User",is_active=True)
    data = [{"first_name":u.first_name, "last_name":u.last_name,"email":u.email} for u in users]
    return JsonResponse(data,safe=False)

def admin_users(request):
    admins = User.objects.filter(role__name="Admin",is_active=True)
    data = [{"first_name":u.first_name, "last_name" : u.last_name, "email" : u.email} for u in admins]
    return JsonResponse(data,safe=False)

def example_users(request):
    users = User.objects.filter(email__endswith="@example.com")
    data = [{"first_name" : u.first_name, "last_name" : u.last_name, "email" : u.email} for u in users]
    return JsonResponse(data,safe=False)

def recent_users(request):
   users = User.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))
   data = [{"first_name": u.first_name, "last_name": u.last_name, "email": u.email} for u in users]
   return JsonResponse(data, safe=False)

def managers_or_users(request):
    users = User.objects.filter(Q(role__name="Manager") | Q(role__name="User"))
    data = [{"first_name": u.first_name, "last_name": u.last_name, "email": u.email} for u in users]
    return JsonResponse(data, safe=False)

def user_access_rules(request):
    rules = AccessRoleRule.objects.filter(role__name="User",element__name="Orders",read_permission=True)
    data = [{"role":r.role.name, "element" : r.element.name, "can_read" : r.read_permission} for r in rules]
    return JsonResponse(data,safe=False)



class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == "Admin"

class AccessRoleRuleViewSet(viewsets.ModelViewSet):
    queryset = AccessRoleRule.objects.all()
    serializer_class = AccessRoleRuleSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        if self.request.user.role.name == "Admin":
            return AccessRoleRule.objects.all()
        return AccessRoleRule.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role.name != "Admin":
            return Response({"error" : "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role.name != "Admin":
            return Response({"error" : "Forbidden"},status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role.name != "Admin":
            return Response({"error" : "Forbidden"}, status = status.HTTP_403_FORBIDDEN)
        instance.delete()


# Create your views here.
