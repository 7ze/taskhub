from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Task


def tasks(request):
    tasks = Task.objects.filter(
        Q(created_by=request.user) | Q(assignee=request.user)
    ).all()
    return render(request, "tasks/index.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_by = request.user
            description = form.cleaned_data.get("description", "")
            new_task.description = (
                description if description else "No description provided."
            )
            if new_task.due_date < timezone.now().date():
                error_message = "Due date must be in the future."
                return render(
                    request,
                    "tasks/create_task.html",
                    {"form": form, "error_message": error_message},
                )
            new_task.save()
            return redirect("tasks:tasks")  # Redirect to the tasks page
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html", {"form": form})
