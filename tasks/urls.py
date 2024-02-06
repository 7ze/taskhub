from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.tasks, name="tasks"),
    path("create/", views.create_task, name="create_task"),
]
