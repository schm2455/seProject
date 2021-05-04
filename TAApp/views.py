from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views import View
from TAApp.models import MyUser, Administrator, Instructor, TA, Course


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):

        if MyUser.objects.filter(name=request.POST['name']).exists():
            user = MyUser.objects.get(name=request.POST['name'])

            if user.password == request.POST['password']:
                if user.role == "Admin":
                    return render(request, 'admin_home.html')
                elif user.role == "Instructor":
                    return render(request, 'admin_home.html')
                elif user.role == "TA":
                    return render(request, 'TA_home.html')
                else:
                    return render(request, 'admin_home.html')
            else:
                return render(request, 'login.html', {"message": "Bad Password"})
        else:
            return render(request, 'login.html', {"message": "No Such User"})


class Admin_home(View):
    def get(self, request):
        m = request.session["name"]
        courses = list(map(str), Course.objects.filter())
        tas = list(map(str), TA.objects.filter(owner__name=m))
        return render(request, "admin_home.html", {"name": m, "Courses": courses, "TAList": tas, "AssignmentList": None})


class Courses(View):
    def get(self, request):
        return render(request, "courses.html", {})

    def post(self, request):
        coursename = request.POST['name']
        teacher = request.POST['instructor']
        TAman = request.POST['instructorTA']
        desc = request.POST['description']

        if coursename is None or teacher is None or TAman is None or desc is None:
            return render(request, "courses.html", {"message": "Please fill all the boxes."})

        Course.objects.create(name=coursename, description=desc, instructor=Instructor.objects.create(name=teacher),
                              instructorTA=TA.objects.create(name=TAman))
        user = MyUser.role
        if user == "Admin":
            return render(request, 'admin_home.html', {"message": "Success!"})
        elif user == "Instructor":
            return render(request, 'admin_home.html', {"message": "Success!"})
        else:
            return render(request, 'admin_home.html', {"message": "Success!"})


class Register(View):
    def get(self, request):
        return render(request, "register.html", {})

    def post(self, request):
        newUser = request.POST['name']
        newUserPass = request.POST['password']
        userWork = request.POST['job']
        if not MyUser.objects.filter(name=request.POST['name']).exists():
            if userWork != 'Select...':
                MyUser.objects.create(name=newUser, password=newUserPass, role=userWork)
                MyUser.save()

            else:
                return render(request, "register.html", {"message": "Please try again!"})
        else:
            return render(request, "register.html", {"message": "Duplicate user"})
        print("Successfully added!")
        return render(request, "login.html", {"message": "Success!"})


class TA_home(View):
    def get(self, request):
        return render(request, "TA_home.html", {})

    def post(self, request):
        return redirect('/admin_home/')
