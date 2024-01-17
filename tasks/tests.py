from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TaskCreationTests(TestCase):
    def test_successful_task_creation(self):
        response = self.client.post(
            reverse("task:create"),
            {
                "title": "Complete Project Proposal",
                "description": "Draft and submit the project proposal by end of the week.",
                "due_date": "2024-02-07",
                "assignee": "Max",
            },
        )
        self.assertEqual(response.status_code, 200)
        new_task = Task.objects.get(title="Complete Project Proposal")
        self.assertIsNotNone(new_task)
        self.assertEqual(
            new_task.description,
            "Draft and submit the project proposal by end of the week.",
        )
        self.assertEqual(new_task.due_date, date(2024, 2, 7))
        self.assertEqual(new_task.assignee, "Max")

    def test_task_title_requirement(self):
        response = self.client.post(
            reverse("task:create"),
            {
                "title": "",
                "description": "Draft and submit the project proposal by end of the week.",
                "due_date": "2024-02-07",
                "assignee": "Max",
            },
        )
        self.assertEqual(response.status_code, 200)
        error_message = "This field is required."
        self.assertContains(response, error_message)

    def test_prevent_past_due_task_creation(self):
        response = self.client.post(
            reverse("task:create"),
            {
                "title": "First task",
                "description": "Draft and submit the project proposal by end of the week.",
                "due_date": (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
                "assignee": "Max",
            },
        )
        self.assertEqual(response.status_code, 200)
        error_message = "Due date must be in the future."
        self.assertContains(response, error_message)

    def test_successful_task_creation_with_optional_description(self):
        response = self.client.post(
            reverse("task:create"),
            {
                "title": "First task",
                "description": "",
                "due_date": "2024-02-07",
                "assignee": "Max",
            },
        )
        self.assertEqual(response.status_code, 200)
        new_task = Task.objects.get(title="First task")
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.description, "")

    def test_successful_task_creation_without_assignee(self):
        response = self.client.post(
            reverse("task:create"),
            {
                "title": "First task",
                "description": "Do this task",
                "due_date": "2024-02-07",
                "assignee": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        new_task = Task.objects.get(title="First task")
        self.assertIsNotNone(new_task)
        self.assertIsNone(new_task.assignee)
