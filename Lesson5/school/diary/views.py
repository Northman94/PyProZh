from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

user_list = []
new_user = User()

def login(request):
    if request.method == 'POST':
        l_name = request.POST.get('username')
        l_password = request.POST.get('password')

        if user_list:
            print(f"User_LIST: {user_list}")
            for user in user_list:
                print(f"User iter: {user}")
                if user.name == l_name and user.password == l_password:
                    print(f"REDIRECT TO SHOW PROFILE")
                    return redirect(show_profile)

        print(f"CREATING NEW USER")
        new_user.name = l_name
        new_user.password = l_password

        user_list.append(new_user)
        print(f"new_user: {new_user}")
        print(f"user_list: {user_list}")
        print(f"SHOW PROFILE")
        return redirect(show_profile)
    print(f"RENDER LOGIN")
    return render(request, 'login.html')


def show_profile(request):
    if user_list:
        print("User list is not EMPTY")
        print(f"new_user: {new_user}")
        print(f"user_list: {user_list}")
        user = user_list[0]  # Assuming only one user is logged in at a time
        return render(request, 'profile.html', {'user': user})
    else:
        return HttpResponse('No user found.')


def delete_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        for user in user_list:
            if user.name == username and user.password == password:
                user_list.remove(user)
                return redirect(delete_success)

        return HttpResponse('Invalid credentials. Please try again.')

    return render(request, 'delete.html')


def delete_success(request):
    return render(request, 'delete.html', {'message': 'User Deleted'})