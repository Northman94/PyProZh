# tests.py
from django.test import TestCase
from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerysetEqual, assertTemplateUsed
from .models import Note


@pytest.mark.urls("scheduler.urls")
def test_login_route(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")
















