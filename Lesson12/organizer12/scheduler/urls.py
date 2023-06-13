# scheduler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name= "login"),
    path("login/", views.login_view, name= "login"),
    path("alter/", views.alter_user, name="alter_user"),
    path("profile/", views.show_profile, name="show_profile"),

    path("delete/", views.delete_profile, name="delete_profile"),
    path("logout/", views.logout_view, name="logout_user"),

    path("note/", views.user_notes, name="user_notes"),
    path("note/<int:note_id>/", views.show_note_details, name="note_details"),

    # Admin paths:
    path("users/", views.admin_see_user, name="see_user"),
    path("users/<str:username>/", views.admin_user_info, name="user_info"),
    path("note/<str:username>/<int:note_id>/", views.admin_user_notes, name="admin_note"),
]
