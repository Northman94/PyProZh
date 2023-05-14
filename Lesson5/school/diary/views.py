from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from .models import User


user = User(name="", password="", language="", grade="")


def login(request):
    global user

    if request.method == 'POST':
        # Info local save from HTML-Form:
        l_name = request.POST.get('username')
        l_password = request.POST.get('password')

        # Log-In Button Pressed:
        if request.POST.get('action') == 'Login':
            if check_user_in_db(l_name, l_password):
                # User Present:
                return redirect(show_profile)
            else:
                # User Absent:
                return render(request, 'login.html', {'message': 'No such User.'})


        # Register Button Pressed:
        if request.POST.get('action') == 'Register':
            # Check if user PRESENT in DB:
            if check_user_in_db(l_name, l_password):
                return render(request, 'login.html', {'message': 'Username already exists.'})
            else:
                # Create a NEW USER
                user = User(name=l_name, password=l_password)
                user.save()
                return redirect(show_profile)

    return render(request, 'login.html')


def show_profile(request):
    global user

    if request.method == 'POST':
        if request.POST.get('action') == 'Change User':
            return redirect(login)

        if request.POST.get('action') == 'Delete User':
            user = User.objects.all().filter(name=user.name, password=user.password)
            user.delete()
            return redirect(delete_profile)

    return render(request, 'profile.html', {'user': user})


def check_user_in_db(c_name, c_password):

    # SHOULD FILL HERE ALL FIELDS FROM DB:
    db_content = User.objects.all()

    # Iterate through each user
    for db_item in db_content:
        # Check if the username matches the search criteria:
        if db_item.name == c_name and db_item.password == c_password:
            # Assign the user's fields to variables:
            user.name = db_item.name
            user.password = db_item.password
            user.language = db_item.language
            user.grade = db_item.grade
            return True

    return False


def delete_profile(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'Return to Login':
            return redirect(login)

    return render(request, 'delete.html')
