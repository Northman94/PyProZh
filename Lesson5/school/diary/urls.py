# diary/urls.py
from django.urls import path
from .views import login, delete_profile

urlpatterns = [
    path('login/', login, name='login'),
    path('delete/', delete_profile, name='delete'),
]
