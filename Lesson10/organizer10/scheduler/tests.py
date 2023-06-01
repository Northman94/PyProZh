# tests.py
from django.test import TestCase
from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerysetEqual, assertTemplateUsed
from .models import MyUser, Note


@pytest.mark.urls("scheduler.urls")
def test_login_route(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")\



@pytest.mark.django_db
@pytest.mark.urls("scheduler.urls")
def test_user_have_single_note(client):
    name = "User1"
    password = "cryptography_staff_123"
    language = "Polish"
    grade = "Low"

    # Create a user in DB
    single_note_user = MyUser.objects.create(
        name=name,
        password=password,
        language=language,
        grade=grade
    )

    # Create a note associated with the user
    new_note = Note.objects.create(
        user_note=single_note_user,
        title="Test Note",
        msg="This is a test note",
        assignee="Test User",
        e_mail="Test_Email@ithillel.ua"
    )

    assert single_note_user is not None
    assert new_note is not None

    # Access the user's notes page
    response = client.get(reverse("user_info", kwargs={"username": new_note.user_note}))
    assert response.status_code == 200
    assertTemplateUsed(response, "admin_user_info.html")

    # Check if the note is present in the response
    assert new_note.title in response.content.decode()

    # We are on page: http://127.0.0.1:8000/users/John/
    # Only user info here and Note titles


