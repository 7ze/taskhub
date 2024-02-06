from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:  # type: ignore
        model = Task
        fields = ["title", "description", "due_date", "assignee"]
