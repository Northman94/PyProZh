# diary/views.py
from django.shortcuts import render
from django.http import HttpResponse

# Sample user data
users = [
    {
        'name': 'Elon Musk',
        'password': '1234',
        'language': 'English',
        'grade': 85
    },
    {
        'name': 'Joane Rowling',
        'password': '4321',
        'language': 'Spanish',
        'grade': 92
    }
]


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        for user in users:
            if user['name'] == username and user['password'] == password:
                return render(request, 'profile.html', {'user': user})

        return HttpResponse('Invalid credentials. Please try again.')

    return render(request, 'login.html')


def delete_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        for user in users:
            if user['name'] == username and user['password'] == password:
                users.remove(user)
                return HttpResponse('Profile deleted successfully.')

        return HttpResponse('Invalid credentials. Please try again.')

    return render(request, 'delete.html')

