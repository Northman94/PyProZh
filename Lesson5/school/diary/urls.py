from django.urls import path
from .views import login, show_profile, delete_profile, delete_success

urlpatterns = [
    path('', login, name='login'),
    path('login/', login, name='login'),
    path('profile/', show_profile, name='profile'),  # Add this line
    path('delete/', delete_profile, name='delete'),
    path('delete/success/', delete_success, name='delete_success'),
]
