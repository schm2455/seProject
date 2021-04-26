from django.shortcuts import render, redirect
from django.views import View
from TAApp.models import MyUser
from django.contrib.auth.forms import UserCreationForm


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        return redirect("admin_home/")


class Admin_home(View):
    def get(self, request):
        return render(request, "admin_home.html", {})


def register(request):
    form = UserCreationForm
    return render(request, "register.html", context={"form": form})
