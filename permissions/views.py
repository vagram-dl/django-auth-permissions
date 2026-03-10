from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from permissions.models import User, AccessRoleRule


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


# Create your views here.
