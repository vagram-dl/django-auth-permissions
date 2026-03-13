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
from django.urls import path, include
from permissions.views import active_users
from django.http import JsonResponse
from permissions import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from permissions.views import AccessRoleRuleViewSet

from permissions.views import (
    RegisterView, LoginView, ProfileView, LogoutView,
    UpdateUserView,DeleteUserView,AccessRuleView,
    active_users,admin_users,example_users,
    recent_users, managers_or_users, user_access_rules
)

def home(request):
    return JsonResponse({"message":"Добро пожаловать в API!"})

router = DefaultRouter()
router.register(r'access-rules', AccessRoleRuleViewSet, basename='access-rules')

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
    path('register/',RegisterView.as_view(), name = 'register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('update/',UpdateUserView.as_view(),name='update_user'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
    path('access-rules/', AccessRuleView.as_view(),name = 'access_rules'),
    path('users/active/', active_users, name = 'active_users'),
    path('users/admin/',admin_users, name = 'admin_users'),
    path('users/example',example_users, name = 'example_users'),
    path('users/managers-or-users/', managers_or_users, name = 'managers_or_users'),
    path('users/access-rules/',user_access_rules, name = 'user-access-rules'),
    path('',include(router.urls)),
]
