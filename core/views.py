from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from .forms import UserSignUpForm


def index(request):
    return render(request, "core/index.html")


def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:login")
    else:  # else is needed to render form on errors in POST
        form = UserSignUpForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("core:index")
