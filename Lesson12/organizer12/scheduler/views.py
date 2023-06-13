# scheduler/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from random import randint
from .forms import NoteForm
from .models import MyUser, Note
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from colorama import Fore


def login_view(request):
    if request.method == "POST":
        # Info from login HTML-Form:
        l_name = request.POST.get("username")
        l_password = request.POST.get("password")

        # Log-In Button Pressed:
        if request.POST.get("action") == "Login":
            # User Present:
            if authenticate(username=l_name, password=l_password):
                print(Fore.RED + "USER AUTHENTICATED !!!!!!!!!!!!!!!\n")
                return redirect(show_profile)
            else:
                # User Absent:
                return render(request, "login.html", {"message": "No such User."})

        # Register Button Pressed:
        if request.POST.get("action") == "Register":
            # Check if user is PRESENT in DB:
            if User.objects.filter(username=l_name).exists():
                return render(
                    request, "login.html", {"message": "Username already exists."}
                )
            else:
                # Create USER partially to have filled suggestions in the next form
                l_user = User.objects.create_user(username=l_name, password=l_password)
                return redirect(alter_user)


    # RENDER LOGIN
    return render(request, "login.html")


def alter_user(request):
    if request.method == "POST":
        a_username = request.POST.get("username")
        a_password = request.POST.get("password")
        a_language = request.POST.get("language")
        a_grade = get_grade(randint(1, 10))

        if request.POST.get("action") == "Next":
            a_user = User.objects.get(username=a_username)

            # Update user's password
            a_user.set_password(a_password)
            a_user.save()

            # Get or create MyUser instance
            my_user, _ = MyUser.objects.get_or_create(my_user=a_user)
            my_user.language = a_language
            my_user.grade = a_grade
            my_user.save()

            print("USER UPDATED/CREATED !!!!!!!!!!!!")
            return redirect(show_profile)

    return render(request, "alter.html", {"user": request.user})






def show_profile(request):
    print(f"SHOW PROFILE !!!!!!!!!!!!!!!")
    if request.method == "POST":
        if request.POST.get("action") == "Change User Info":
            return redirect(alter_user)

        if request.POST.get("action") == "Delete User":
            user = User.objects.get(username=request.user.username)
            user.delete()
            return redirect(delete_profile)

        if request.POST.get("action") == "Logout":
            return redirect(logout_view)

        # Create/Show NOTES page:
        if request.POST.get("action") == "NOTES":
            return redirect(user_notes)

    # RENDER PROFILE
    return render(request, "profile.html", {"user": request.user})


def delete_profile(request):
    if request.method == "POST":
        if request.POST.get("action") == "Return to Login":
            return redirect(login_view)

    # RENDER DELETE
    return render(request, "delete.html")


def get_grade(level):
    if level < 4:
        return "Low"
    elif level < 7:
        return "Medium"
    else:
        return "High"


def user_notes(request):
    # Check/Update user from DB:
    person = MyUser.objects.get(my_user=request.user)
    notes = Note.objects.filter(user_note=person)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note_title = form.cleaned_data["title"]
            new_note_msg = form.cleaned_data["msg"]
            new_note_assignee = form.cleaned_data["assignee"]
            new_note_e_mail = form.cleaned_data["e_mail"]

            Note.objects.create(
                user_note=person,
                title=new_note_title,
                msg=new_note_msg,
                assignee=new_note_assignee,
                e_mail=new_note_e_mail,
            )
            print("Note created")
            # Redirect to refresh the page after creating a note
            return redirect(user_notes)
    else:
        form = NoteForm()

    print("User/Notes List info")
    return render(request, "user_notes.html", {"notes": notes, "form": form})


def show_note_details(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, "note_details.html", {"note": note})


# Admin part Requests:
# path('users/'...
def admin_see_user(request):
    template = loader.get_template("admin_user_list_base.html")
    context = {"users": MyUser.objects.all()}
    return HttpResponse(template.render(context, request))


# path('users/<str:username>/'...
# "username" parameter is passed from the path of "scheduler/urls.py" file
def admin_user_info(request, username):
    admin_usr = get_object_or_404(MyUser, my_user__username=username)
    notes = Note.objects.filter(user_note=admin_usr)

    return render(
        request,
        "admin_user_info.html",
        {
            "username": username,
            "language": admin_usr.language,
            "grade": admin_usr.grade,
            "notes": notes,
        },
    )


# path('note/<str:username>/<int:note_id>/'...
def admin_user_notes(request, username, note_id):
    note = get_object_or_404(Note, id=note_id, user_note__my_user__username=username)
    return render(
        request, "admin_user_notes.html", {"note": note, "username": username}
    )


def logout_view(request):
    logout(request)
    return redirect(login_view)
