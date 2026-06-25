from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('csrf-token', views.get_csrf_token, name='csrf-token'),
    path('login', csrf_exempt(views.user_login), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('check-login', views.check_login, name='check-login'),
    path('user/profile', views.user_profile, name='user-profile'),
    path('user/change-password', views.change_password, name='change-password'),
]
