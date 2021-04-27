from django.shortcuts import render, redirect
from django.views import View
from TAApp.models import MyUser, Course, TA, Administrator


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = MyUser.objects.get(name=request.POST['name'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if request.POST['name'] == "Admin" and request.POST['password'] == "Admin":
            return redirect("/admin_home/")
        if request.POST['name'] == "Admin" and request.POST['password'] != "Admin":
            return render(request, "login.html", {"message": "bad password"})
        elif noSuchUser:
            return render(request, "login.html", {"message": "No such user."})
        elif badPassword:
            return render(request, "login.html", {"message": "bad password"})
        else:
            return render(request, "login.html", {"message": "login failed"})


class Admin_home(View):
    def get(self, request):
        return render(request, "admin_home.html", {})

    def post(self, request):
        if request.method == 'POST' and 'TA' in request.post:
            tName = request.POST.get('TA', '')
            newTA = TA(name=tName, project_manager='Admin')
            newTA.save()
        tas = list(map(str, TA.objects.filter(name='Admin')))
        return render(request, "admin_home.html", {'name': tName, 'tas': tas})


class Courses(View):
    def get(self, request):
        return render(request, "courses.html", {})


class Register(View):
    def get(self, request):
        return render(request, "register.html", {})


class TA_home(View):
    def get(self, request):
        return render(request, "TA_home.html", {})
    def post(self, request):

        return redirect('/admin_home/')
