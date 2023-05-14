# diary/urls.py
from django.urls import path
from .views import login, show_profile, delete_profile

urlpatterns = [
    path('', login, name='login'),
    path('login/', login, name='login'),
    path('profile/', show_profile, name='profile'),
    path('delete/', delete_profile, name='delete'),
]
