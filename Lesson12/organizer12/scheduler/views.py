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


def login(request):

    if request.method == "POST":
        # Info from login HTML-Form:
        l_name = request.POST.get("username")
        l_password = request.POST.get("password")

        # Log-In Button Pressed:
        if request.POST.get("action") == "Login":
            # User Present:
            if authenticate(username = l_name, password = l_password):
                print(Fore.RED + "USER AUTHENTICATED !!!!!!!!!!!!!!!\n")
                return redirect(show_profile)
            else:
                # User Absent:
                return render(request, "login.html", {"message": "No such User."})

        # Register Button Pressed:
        if request.POST.get("action") == "Register":
            # # Check if user PRESENT in DB:
            # if check_user_in_db(l_name, l_password):
            #     return render(
            #         request, "login.html", {"message": "Username already exists."}
            #     )
            # else:
            # Create USER partially to have filled suggestions in the next form
            l_user = User.objects.create_user(username=l_name, password=l_password)

            if l_user is not None:
                print(f"User {l_user}")
            else:
                print("???????????????????????????")
            return redirect(alter_user)

    # RENDER LOGIN
    return render(request, "login.html")


# Clears the user's session and removes the authentication information:
def logout_view(request):
    logout(request)
    return redirect(login)


# @login_required(login_url="login/")
def alter_user(request):

    if request.method == "POST":
        print(Fore.RED + f"POST from alter_user!!!!!!!!")
        # Info from alter HTML-Form:
        a_name = request.POST.get("username")
        a_password = request.POST.get("password")
        a_language = request.POST.get("language")
        a_grade = get_grade(randint(1, 10))

        if request.POST.get("action") == "Next":
            if check_user_in_db(a_name, a_password):
                print(Fore.RED + f"NEXT check in DB!!!!!!!!")

                # User present in DB => update fields
                # Avoiding New Instance Creation
                db_user = MyUser.objects.filter(name=user.name, password=user.password).first()
                db_user.name = a_name
                db_user.password = a_password
                db_user.language = a_language
                db_user.grade = a_grade
                # Updating info for forms
                user.name = a_name
                user.password = a_password
                user.language = a_language
                user.grade = a_grade
                print(Fore.RED + f"USER SAVED!!!!!!!!")
                db_user.save()
            else:
                print(Fore.RED + f"NEXT NOT in DB!!!!!!!!")
                # Create a new user
                user.name = a_name
                user.password = a_password
                user.language = a_language
                user.grade = a_grade

                user.save()

            print(Fore.RED + f"TO SHOW PROFILE!!!!!!!!")
            return redirect(show_profile)

    print(Fore.RED + f"RENDER ALTER !!!!!!!!!!!!!!!!!!!!")
    return render(request, "alter.html", {"user": request.user})


#@login_required(login_url="login/")
def show_profile(request):
    print(f"SHOW PROFILE !!!!!!!!!!!!!!!")
    if request.method == "POST":
        if request.POST.get("action") == "Change User Info":
            return redirect(alter_user)

        if request.POST.get("action") == "Delete User":
            user = MyUser.objects.filter(name=User.username, password=User.password).first()
            user.delete()
            return redirect(delete_profile)

        if request.POST.get("action") == "Logout":
            return redirect(logout_view)

        # Create/Show NOTES page:
        if request.POST.get("action") == "NOTES":
            return redirect(user_notes)

    # RENDER PROFILE
    return render(request, "profile.html", {"user": request.user})


def check_user_in_db(c_name, c_password):
    global user

    # FILTERED FIELDS FROM DB:
    db_content = MyUser.objects.filter(name=c_name, password=c_password).first()

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

    # RENDER DELETE
    return render(request, "delete.html")


def get_grade(level):
    if level < 4:
        return "Low"
    elif level < 7:
        return "Medium"
    else:
        return "High"


#@login_required(login_url="login/")
def user_notes(request):
    # Check/Update user from DB:
    person = MyUser.objects.filter(name=user.name).first()
    notes = Note.objects.filter(user_note=person.id)

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


#@login_required(login_url="login/")
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
# "username" parameter is passed from path of "scheduler/urls.py" file
def admin_user_info(request, username):
    admin_usr = get_object_or_404(MyUser, name=username)
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
    note = get_object_or_404(Note, id=note_id, user_note__name=username)
    return render(
        request, "admin_user_notes.html", {"note": note, "username": username}
    )
