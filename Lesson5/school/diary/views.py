from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from .models import User
from random import randint


user = User(name="", password="", language="", grade="")


def login(request):
    global user

    if request.method == 'POST':
        # Info local save from HTML-Form:
        l_name = request.POST.get('username')
        l_password = request.POST.get('password')

        # Log-In Button Pressed:
        if request.POST.get('action') == 'Login':
            print("LOGIN PRESSED")

            if check_user_in_db(l_name, l_password):
                # User Present:
                print("User Present")
                return redirect(show_profile)
            else:
                # User Absent:
                print("User Absent")
                return render(request, 'login.html', {'message': 'No such User.'})


        # Register Button Pressed:
        if request.POST.get('action') == 'Register':
            print("REGISTER PRESSED")
            # Check if user PRESENT in DB:
            if check_user_in_db(l_name, l_password):
                return render(request, 'login.html', {'message': 'Username already exists.'})
            else:
                # Create USER partially to have filled suggestions in next form
                print("CREATE NEW LOCAL PRE USER")
                user = User(name=l_name, password=l_password)

                return redirect(alter_user)

    print("RENDER LOGIN")
    return render(request, 'login.html')


def alter_user(request):
    global user
    print("SET/ALTER PROFILE")

    if request.method == "POST":
        a_name = request.POST.get('username')
        a_password = request.POST.get('password')
        a_language = request.POST.get('language')
        a_grade = get_grade(randint(1, 10))

        if request.POST.get('action') == 'Next':
            if check_user_in_db(a_name, a_password):
                # User present in DB - update fields
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

    return render(request, 'alter.html', {'user': user})



def show_profile(request):
    global user
    print("SHOW PROFILE")

    if request.method == 'POST':
        print("SHOW PR POST")
        if request.POST.get('action') == 'Change User':
            print("CHANGE USER")
            return redirect(alter_user)

        if request.POST.get('action') == 'Delete User':
            print("DELETE USER")
            user = User.objects.filter(name=user.name, password=user.password).first()
            user.delete()
            return redirect(delete_profile)

    print("RENDER PR")
    return render(request, 'profile.html', {'user': user})


def check_user_in_db(c_name, c_password):
    global user
    print("CHECK USER!!!!!")

    # SHOULD FILL HERE ALL FIELDS FROM DB:
    db_content = User.objects.filter(name=c_name, password=c_password).first()
    print(f"DB CONTAINER: {db_content}")
    if db_content:
        # Assign the user's fields to variables:
        user.name = db_content.name
        user.password = db_content.password
        user.language = db_content.language
        user.grade = db_content.grade
        return True
    return False


def delete_profile(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'Return to Login':
            print("RETURN TO LOGIN FROM DEL")
            return redirect(login)

    print("RENDER DELETE PR")
    return render(request, 'delete.html')


def get_grade(level):
    if level < 4:
        return 'Low'
    elif level < 7:
        return 'Medium'
    else:
        return 'High'