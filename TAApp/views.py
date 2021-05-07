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
                    return redirect('/admin_home/')
                elif user.role == "Instructor":
                    return redirect('/Instructor_home')
                elif user.role == "TA":
                    return redirect('/TA_home/')
                else:
                    return redirect('/admin_home/')
            else:
                return render(request, 'login.html', {"message": "Bad Password"})
        else:
            return render(request, 'login.html', {"message": "No Such User"})


class Admin_home(View):
    def get(self, request):
        TAList = list(map(str, TA.objects.all()))
        InstructorList = list(map(str, Instructor.objects.all()))
        CourseList = list(map(str, Course.objects.all()))

        return render(request, "admin_home.html", {"tas": TAList, "instructors": InstructorList, "courses":CourseList})


class Courses(View):
    def get(self, request):
        instructors = list(map(str, Instructor.objects.all()))
        tachoices = list(map(str, TA.objects.all()))
        return render(request, "courses.html", {"instructors": instructors, "tachoices": tachoices})

    def post(self, request):
        coursename = request.POST['name']
        instructorname = request.POST['instructorchoice']
        taname = request.POST['tachoice']
        desc = request.POST['description']

        if coursename is None or instructorname == "Select..." or taname == "Select..." or desc is None:
            return render(request, "courses.html", {"message": "Please fill all the boxes."})

        instructorchoice = Instructor.objects.get(name=instructorname)
        tachoice = TA.objects.get(name=taname)

        Course.objects.create(name=coursename, description=desc, instructor=instructorchoice, instructorTA=tachoice)
        user = MyUser.role
        if user == "Admin":
            return redirect('/admin_home/', {"message": "Success!"})
        elif user == "Instructor":
            return redirect('/admin_home/', {"message": "Success!"})
        else:
            return redirect('/admin_home/', {"message": "Success!"})


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
                if userWork == "Instructor":
                    Instructor.objects.create(name=newUser)
                elif userWork == "TA":
                    TA.objects.create(name=newUser)
            else:
                return render(request, "register.html", {"message": "Please try again!"})
        else:
            return render(request, "register.html", {"message": "Duplicate user"})
        print("Successfully added!")
        return render(request, "login.html", {"message": "Success!"})

class whatCourse(View):
    def get(self,request):
        cour = request.GET.get("name")

        myCourse = Course.objects.get(name = cour)
        desc = myCourse.description
        name = myCourse.name
        inst = myCourse.instructor
        tadude = myCourse.instructorTA

        return render(request, "thiscourse.html", {"desc":desc,"name":name,"inst":inst,"tadude":tadude})

    def post(self,request):
        return None

class CreateTA(View):
    def get(self, request):
        return render(request, "TAs.html", )

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


class TA_home(View):
    def get(self, request):
        return render(request, "TA_home.html", {})

class Instructor_home(View):
    def get(self, request):
        return render(request, "Instructor_home.html", {})


class CreateInstructor(View):
    def get(self, request):
        return render(request, "instructors.html", {})

    def post(self, request):
        instructorname = request.POST.get('instructor')

        if instructorname is None:
            return render(request, "instructors.html", {"message": "Please fill all the boxes."})
        if Instructor.objects.filter(name=instructorname).exists():
            return render(request, 'instructors.html', {"message": "instructor already exists"})
        if not Administrator.objects.filter(name='Admin').exists():
            Administrator.objects.create(name="Admin", password="Admin")
        projManager = Administrator.objects.get(name="Admin")
        Instructor.objects.create(name=instructorname, project_manager=projManager)
        return render(request, 'admin_home.html', {"message": "Success!"})
