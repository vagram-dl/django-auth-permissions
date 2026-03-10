"""
URL configuration for auth_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from permissions.views import active_users
from django.http import JsonResponse
from permissions import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(request):
    return JsonResponse({"message":"Добро пожаловать в API!"})

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('admin/', admin.site.urls),
    path('active-users/',active_users, name="active_users"),
    path('',home,name="home"),
    path('admin-users/',views.admin_users,name="admin_users"),
    path('example-users/',views.example_users,name="example_users"),
    path('recent-users/',views.recent_users,name="recent_users"),
    path('managers-or-users/',views.managers_or_users,name="managers_or_users"),
    path('user-access-rules/',views.user_access_rules, name="user_access_rules"),
]
