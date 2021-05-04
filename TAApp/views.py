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

class Instructors(View):
    def get(self, request):
        return render(request, "instructors.html", {})

    def post(self, request):
        instructorname = request.POST.get('instructor')
        if instructorname is None:
            return render(request, "instructors.html", {"message": "Please fill all the boxes."})
        if Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'instructors.html',{"message": "instructor already exists"})
        if not Administrator.objects.filter(name='Admin').exists():
            Administrator.objects.create(name="Admin", password="Admin")
        projManager = Administrator.objects.get(name="Admin")
        n=Instructor.objects.create(name=instructorname, project_manager=projManager)
        n.save()
        return render(request, 'admin_home.html', {"message": "Success!"})

class TAs(View):
    def get(self, request):
        tas=list(map(str, TA.objects.all()))
        return render(request, "TAs.html", {"tas":tas})

    def post(self, request):
        taname = request.POST.get('name')
        instructorname = request.POST.get('instructor')

        if instructorname is None or taname is None:
            return render(request, "TAs.html", {"message": "Please fill all the boxes."})
        if TA.objects.filter(name=taname).exists():
            return render(request, 'TAs.html', {"message": "TA already exists"})

        if not Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'TAs.html', {"message": "Instructor does not exist"})
        t=TA.objects.create(name=taname, project_manager=Instructor.objects.get(name=instructorname))
        t.save()
        tas = list(map(str, TA.objects.all()))
        user = MyUser.role
        if user == "Admin":
            return render(request, 'admin_home.html', {"message": "Success!","tas":tas})
        elif user == "Instructor":
            return render(request, 'admin_home.html', {"message": "Success!"})
        else:
            return render(request, 'admin_home.html', {"message": "Success!"})

class Admin_home(View):
    def get(self, request):
        return render(request, "admin_home.html", {})


class Courses(View):
    def get(self, request):
        return render(request, "courses.html", {})

    def post(self, request):
        coursename = request.POST['name']
        instructorname = request.POST['instructor']
        taname = request.POST['instructorTA']
        desc = request.POST['description']

        if coursename is None or instructorname is None or taname is None or desc is None:
            return render(request, "courses.html", {"message": "Please fill all the boxes."})

        Course.objects.create(name=coursename, description=desc, instructor=instructorname, instructorTA=taname)
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

            else:
                return render(request, "register.html", {"message": "Please try again!"})
        else:
            return render(request, "register.html", {"message": "Duplicate user"})
        print("Successfully added!")
        return render(request, "login.html", {"message": "Success!"})


class TA(View):
    def get(self, request):
        return render(request, "TAs.html",)

    def post(self, request):
        taname = request.POST.get('name')
        instructorname = request.POST.get('instructor')

        if instructorname is None or taname is None:
            return render(request, "TAs.html", {"message": "Please fill all the boxes."})
        if TA.objects.filter(name=taname).exists():
            return render(request, 'TAs.html', {"message": "TA already exists"})

        if not Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'TAs.html', {"message": "Instructor does not exist"})
        TA.objects.create(name=taname, project_manager=Instructor.objects.get(name=instructorname))
        user = MyUser.role
        if user == "Admin":
            return render(request, 'admin_home.html', {"message": "Success!"})
        elif user == "Instructor":
            return render(request, 'admin_home.html', {"message": "Success!"})
        else:
            return render(request, 'admin_home.html', {"message": "Success!"})


class Instructor(View):
    def get(self, request):
        return render(request, "instructors.html", {})

    def post(self, request):
        instructorname = request.POST.get('instructor')

        if instructorname is None:
            return render(request, "instructors.html", {"message": "Please fill all the boxes."})
        if Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'instructors.html',{"message": "instructor already exists"})
        if not Administrator.objects.filter(name='Admin').exists():
            Administrator.objects.create(name="Admin", password="Admin")
        projManager = Administrator.objects.get(name="Admin")
        Instructor.objects.create(name=instructorname, project_manager=projManager)
        return render(request, 'admin_home.html', {"message": "Success!"})
