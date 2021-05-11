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
                if direct(user.role) is not None:
                    return redirect(direct(user.role).url)
                else:
                    return redirect('login.html', {"message": "unauthorized access"})
            else:
                return render(request, 'login.html', {"message": "Bad Password"})
        else:
            return render(request, 'login.html', {"message": "No Such User"})


def direct(user_role):
    if user_role == "Admin":
        return redirect('/admin_home/')
    elif user_role == "Instructor":
        return redirect('/instructor_home/')
    elif user_role == "TA":
        return redirect('/TA_home/')
    else:
        return None


class Admin_home(View):
    def get(self, request):
        TAList = list(map(str, TA.objects.all()))
        InstructorList = list(map(str, Instructor.objects.all()))
        CourseList = list(Course.objects.all())
        return render(request, "admin_home.html", {"TAs": TAList, "instructors": InstructorList,"courses":CourseList})


class Courses(View):
    def get(self, request):
        return render(request, "courses.html", {})

    def post(self, request):
        if MyUser.objects.filter(name=request.POST['name']).exists():
            user = MyUser.objects.get(name=request.POST['name'])
        coursename = request.POST['name']
        instructorname = request.POST['instructor']
        taname = request.POST['instructorTA']
        desc = request.POST['description']

        if coursename is None or instructorname is None or taname is None or desc is None:
            return render(request, "courses.html", {"message": "Please fill all the boxes."})

        Course.objects.create(name=coursename, description=desc, instructor=instructorname, instructorTA=taname)
        if direct(user.role) is not None:
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})

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


class CreateTA(View):
    def get(self, request):
        return render(request, "TAs.html", )

    def post(self, request):
        taname = request.POST.get('name')
        instructorname = request.POST.get('instructor')
        if MyUser.objects.filter(name=request.POST['name']).exists():
            user = MyUser.objects.get(name=request.POST['name'])
        if instructorname is None or taname is None:
            return render(request, "TAs.html", {"message": "Please fill all the boxes."})
        if TA.objects.filter(name=taname).exists():
            return render(request, 'TAs.html', {"message": "TA already exists"})

        if not Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'TAs.html', {"message": "Instructor does not exist"})
        TA.objects.create(name=taname, project_manager=Instructor.objects.get(name=instructorname))
        if direct(user.role) is not None:
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})


class TA_home(View):
    def get(self, request):
        return render(request, "TA_home.html", {})


class Instructor_home(View):
    def get(self, request):
        TAList = list(map(str, TA.objects.all()))
        InstructorList = list(map(str, Instructor.objects.all()))
        return render(request, "instructor_home.html", {"TAs": TAList, "instructors": InstructorList})


class CreateInstructor(View):
    def get(self, request):
        return render(request, "instructors.html", {})

    def post(self, request):
        instructorname = request.POST.get('instructor')
        if MyUser.objects.filter(name=request.POST['name']).exists():
            user = MyUser.objects.get(name=request.POST['name'])
        if instructorname is None:
            return render(request, "instructors.html", {"message": "Please fill all the boxes."})
        if Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'instructors.html', {"message": "instructor already exists"})
        if not Administrator.objects.filter(name='Admin').exists():
            Administrator.objects.create(name="Admin", password="Admin")
        projManager = Administrator.objects.get(name="Admin")
        Instructor.objects.create(name=instructorname, project_manager=projManager)
        if direct(user.role) is not None:
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})
