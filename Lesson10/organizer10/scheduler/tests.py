# tests.py
# from django.test import TestCase
from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed  # assertQuerysetEqual
from .models import MyUser, Note


# Test on correct Routing page:
@pytest.mark.urls("scheduler.urls")
def test_login_route(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")
    assert b"Register" in response.content


# Test on single Note for User:
@pytest.mark.django_db
@pytest.mark.urls("scheduler.urls")
def test_user_have_single_note(client):

    # Create a User in DB
    single_note_user = MyUser.objects.create(
        name="User1",
        password="cryptography_staff_123",
        language="Polish",
        grade="Low"
    )

    # Create the User Note in DB:
    new_note = Note.objects.create(
        user_note=single_note_user,
        title="Test Note",
        msg="This is a test note",
        assignee="Test User",
        e_mail="Test_Email@ithillel.ua"
    )

    # Access the user's notes page:
    response = client.get(reverse("user_info", kwargs={"username": new_note.user_note}))
    assert response.status_code == 200
    assertTemplateUsed(response, "admin_user_info.html")

    # Check if the note is present in the response:
    assert new_note.title in response.content.decode()

    # We are on page: http://127.0.0.1:8000/users/John/
    # Only user info here and Note titles


# Test on three Notes for User:
@pytest.mark.django_db
@pytest.mark.urls("scheduler.urls")
def test_user_have_3_notes(client):

    # Create a user in DB:
    multi_note_user = MyUser.objects.create(
        name="David",
        password="cryptography_staff_321",
        language="Esperanto",
        grade="Medium"
    )

    # Create a User Note1 in DB:
    new_note1 = Note.objects.create(
        user_note=multi_note_user,
        title="Holiday Plans",
        msg="Sunbathe on a beach",
        assignee="Evan Tree",
        e_mail="Test_Email1@ithillel.ua"
    )

    # Create a User Note2 in DB:
    new_note2 = Note.objects.create(
        user_note=multi_note_user,
        title="Morning Routine",
        msg="Walk a Dog",
        assignee="Chris Newdawn",
        e_mail="Test_Email2@ithillel.ua"
    )

    # Create a User Note3 in DB:
    new_note3 = Note.objects.create(
        user_note=multi_note_user,
        title="Animal Care",
        msg="Give Meds",
        assignee="Samanta Hopper",
        e_mail="Test_Email3@ithillel.ua"
    )

    # Access the user's notes page ("username" is same for all 3):
    multi_response = client.get(reverse("user_info", kwargs={"username": new_note1.user_note}))
    assert multi_response.status_code == 200
    assertTemplateUsed(multi_response, "admin_user_info.html")

    # Check if all 3 notes are present in the response:
    assert (new_note1.title and new_note2.title and new_note3.title) in multi_response.content.decode()

    # We are on page: http://127.0.0.1:8000/users/David/
    # Only user info here and Note titles
