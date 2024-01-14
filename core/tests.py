from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserRegistrationAuthenticationTests(TestCase):
    def setUp(self):
        # Creating a user for testing
        self.existing_user = User.objects.create_user(
            username="Achraf",
            email="achraf.boudabous@informatik.hs-fulda.de",
            password="Ach123456*",
        )

    def test_successful_user_signup(self):
        response = self.client.post(
            reverse("core:signup"),
            {
                "username": "Achraf",
                "email": "achraf.boudabous@informatik.hs-fulda.de",
                "password1": "Ach123456*",
                "password2": "Ach123456*",
            },
        )
        self.assertEqual(response.status_code, 200)
        new_user = User.objects.get(username="Achraf")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, "achraf.boudabous@informatik.hs-fulda.de")

    def test_prevent_duplicate_email_registration(self):
        response = self.client.post(
            reverse("core:signup"),
            {
                "username": "Achraf",
                "email": "achraf.boudabous@informatik.hs-fulda.de",
                "password1": "Ach123456*",
                "password2": "Ach123456*",
            },
        )
        self.assertEqual(response.status_code, 200)

        error_message = "A user with that username already exists."
        self.assertContains(response, error_message)

    def test_password_constraints_registration(self):
        response = self.client.post(
            reverse("core:signup"),
            {
                "username": "Achraf",
                "email": "achraf.boudabous@informatik.hs-fulda.de",
                "password1": "1234",
                "password2": "1234",
            },
        )
        self.assertEqual(response.status_code, 200)

        error_message = "This password is too short."
        self.assertContains(response, error_message)

    def test_successful_user_login(self):
        response = self.client.post(
            reverse("core:login"),
            {
                "username": "Achraf",
                "password": "Ach123456*",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_prevent_incorrect_user_login(self):
        response = self.client.post(
            reverse("core:login"),
            {
                "username": "Achraf",
                "password": "5588akiu",
            },
        )
        self.assertEqual(response.status_code, 200)

        error_message = "Please enter a correct username and password."
        self.assertContains(response, error_message)
