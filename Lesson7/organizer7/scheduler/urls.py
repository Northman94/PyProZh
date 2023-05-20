# scheduler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('alter/', views.alter_user, name='alter_user'),
    path('profile/', views.show_profile, name='show_profile'),
    path('delete/', views.delete_profile, name='delete_profile'),
    # Admin paths:
    path('users/', views.admin_see_user, name='see_user'),
    path('users/<str:username>/', views.admin_user_info, name='user_info'),
]
