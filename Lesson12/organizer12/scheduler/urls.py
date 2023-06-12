# scheduler/urls.py
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html")),
    path("accounts/login/profile/", views.show_profile, name="show_profile"),
    path("register/", views.register, name = "register_profile"),

    #path("alter/", views.alter_user, name="alter_user"),
    #path("delete/", views.delete_profile, name="delete_profile"),
    path("logout/", views.logout_view, name="logout_user"),

    # Notes:
    path("note/", views.user_notes, name="user_notes"),
    path("note/<int:note_id>/", views.show_note_details, name="note_details"),

    # Admin paths:
    path("users/", views.admin_see_user, name="see_user"),
    path("users/<str:username>/", views.admin_user_info, name="user_info"),
    path("note/<str:username>/<int:note_id>/", views.admin_user_notes, name="admin_note"),
]
