# scheduler/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from .models import User
from random import randint


user = User(name="", password="", language="", grade="")


def login(request):
    global user

    if request.method == "POST":
        # Info from login HTML-Form:
        l_name = request.POST.get("username")
        l_password = request.POST.get("password")

        # Log-In Button Pressed:
        if request.POST.get("action") == "Login":
            # User Present:
            if check_user_in_db(l_name, l_password):
                return redirect(show_profile)
            else:
                # User Absent:
                return render(request, "login.html", {"message": "No such User."})

        # Register Button Pressed:
        if request.POST.get("action") == "Register":
            # Check if user PRESENT in DB:
            if check_user_in_db(l_name, l_password):
                return render(
                    request, "login.html", {"message": "Username already exists."}
                )
            else:
                # Create USER partially to have filled suggestions in the next form
                user = User(name=l_name, password=l_password)
                return redirect(alter_user)

    # RENDER LOGIN
    return render(request, "login.html")


def alter_user(request):
    global user

    if request.method == "POST":
        # Info from alter HTML-Form:
        a_name = request.POST.get("username")
        a_password = request.POST.get("password")
        a_language = request.POST.get("language")
        a_grade = get_grade(randint(1, 10))

        if request.POST.get("action") == "Next":
            if check_user_in_db(a_name, a_password):
                # User present in DB => update fields
                # Avoiding New Instance Creation
                db_user = User.objects.get(id=user.id)
                db_user.name = a_name
                db_user.password = a_password
                db_user.language = a_language
                db_user.grade = a_grade
                # Updating info for forms
                user.name = a_name
                user.password = a_password
                user.language = a_language
                user.grade = a_grade

                db_user.save()
            else:
                # Create a new user
                user.name = a_name
                user.password = a_password
                user.language = a_language
                user.grade = a_grade

                user.save()

            return redirect(show_profile)

    # RENDER ALTER
    return render(request, "alter.html", {"user": user})


def show_profile(request):
    global user

    if request.method == "POST":
        if request.POST.get("action") == "Change User":
            return redirect(alter_user)

        if request.POST.get("action") == "Delete User":
            user = User.objects.filter(name=user.name, password=user.password).first()
            user.delete()
            return redirect(delete_profile)

    print("RENDER PROFILE")
    return render(request, "profile.html", {"user": user})


def check_user_in_db(c_name, c_password):
    global user

    # FILTERED FIELDS FROM DB:
    db_content = User.objects.filter(name=c_name, password=c_password).first()

    if db_content:
        # Assign DB user's fields to variables:
        user.name = db_content.name
        user.password = db_content.password
        user.language = db_content.language
        user.grade = db_content.grade
        return True
    return False


def delete_profile(request):
    if request.method == "POST":
        if request.POST.get("action") == "Return to Login":
            return redirect(login)

    print("RENDER DELETE")
    return render(request, "delete.html")


def get_grade(level):
    if level < 4:
        return "Low"
    elif level < 7:
        return "Medium"
    else:
        return "High"


def see_user(request):
    all_usrs = User.objects.all()
    return HttpResponse(all_usrs)
