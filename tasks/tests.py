from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Task
from .views import create_task


class TaskCreationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="Achraf",
            email="achraf.boudabous@informatik.hs-fulda.de",
            password="Ach123456*",
        )

    def test_successful_task_creation(self):
        request = self.factory.post(
            reverse("tasks:create_task"),
            {
                "title": "Complete Project Proposal",
                "description": "Draft and submit the project proposal by end of the week.",
                "due_date": date(2024, 2, 7),
                "assignee": self.user.id,  # type: ignore
            },
        )
        request.user = self.user
        response = create_task(request)

        # check if the response is a redirect
        self.assertEqual(response.status_code, 302)

        redirected_page = response.url  # type: ignore
        self.assertEqual(redirected_page, reverse("tasks:tasks"))

        new_task = Task.objects.get(title="Complete Project Proposal")
        self.assertIsNotNone(new_task)
        self.assertEqual(
            new_task.description,  # type: ignore
            "Draft and submit the project proposal by end of the week.",
        )
        self.assertEqual(new_task.due_date, date(2024, 2, 7))  # type: ignore
        self.assertEqual(new_task.assignee, self.user)  # type: ignore

    def test_task_title_requirement(self):
        request = self.factory.post(
            reverse("tasks:create_task"),
            {
                "description": "Draft and submit the project proposal by end of the week.",
                "due_date": date(2024, 2, 7),
                "assignee": self.user.id,  # type: ignore
            },
        )
        request.user = self.user
        response = create_task(request)

        self.assertEqual(response.status_code, 200)

        error_message = "This field is required."
        self.assertContains(response, error_message)

    def test_prevent_past_due_task_creation(self):
        request = self.factory.post(
            reverse("tasks:create_task"),
            {
                "title": "First task",
                "description": "First task description.",
                "due_date": date.today() - timedelta(days=1),
                "assignee": self.user.id,  # type: ignore
            },
        )
        request.user = self.user
        response = create_task(request)

        self.assertEqual(response.status_code, 200)
        error_message = "Due date must be in the future."
        self.assertContains(response, error_message)

    def test_successful_task_creation_with_optional_description(self):
        request = self.factory.post(
            reverse("tasks:create_task"),
            {
                "title": "First task",
                "due_date": date(2024, 2, 7),
                "assignee": self.user.id,  # type: ignore
            },
        )
        request.user = self.user
        response = create_task(request)

        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(title="First task")

        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.description, "No description provided.")

    def test_successful_task_creation_without_assignee(self):
        request = self.factory.post(
            reverse("tasks:create_task"),
            {
                "title": "First task",
                "description": "Do this task.",
                "due_date": date(2024, 2, 7),
            },
        )
        request.user = self.user
        response = create_task(request)

        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(title="First task")

        self.assertIsNotNone(new_task)
        self.assertIsNone(new_task.assignee)
