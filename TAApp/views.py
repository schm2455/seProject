from django.shortcuts import render, redirect
from django.views import View
from TAApp.models import MyUser


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})


class Admin_home(View):
    def get(self, request):
        return render(request, "admin_home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = MyUser.objects.get(name=request.POST['name'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            m = MyUser(name=request.POST['name'], password=request.POST['password'])
            m.save()
            request.session["name"] = m.name
            return redirect("/things/")
        elif badPassword:
            return render(request, "login.html", {"message": "bad password"})
        else:
            request.session["name"] = m.name
            return redirect("/things/")
