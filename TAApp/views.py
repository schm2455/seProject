from django.shortcuts import render, redirect
from django.views import View
from TAApp.models import MyUser


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        return redirect("admin_home/")


class Admin_home(View):
    def get(self, request):
        return render(request, "admin_home.html", {})


class Courses(View):
    def get(self, request):
        return render(request, "courses.html", {})


class Register(View):
    def get(self, request):
        return render(request, "register.html", {})


class TA_home(View):
    def get(self, request):
        return render(request, "TA_home.html", {})
