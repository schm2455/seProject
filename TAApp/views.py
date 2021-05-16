from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from TAApp.models import MyUser, Administrator, Instructor, TA, Course, Lab
from django.core import serializers


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):

        if MyUser.objects.filter(name=request.POST['name']).exists():
            user = MyUser.objects.get(name=request.POST['name'])
            request.session["name"] = user.name
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


def valid(user_role, expected):
    if user_role == expected:
        return True
    else:
        return False


class Admin_home(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        if valid(user.role, "Admin"):
            TAList = list(map(str, TA.objects.all()))
            InstructorList = list(map(str, Instructor.objects.all()))
            CourseList = list(Course.objects.all())
            return render(request, "admin_home.html",
                          {"TAs": TAList, "instructors": InstructorList, "courses": CourseList})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})


class Courses(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        if valid(user.role, "Admin") or valid(user.role, "Instructor"):
            instructors = list(map(str, Instructor.objects.all()))
            tachoices = list(map(str, TA.objects.all()))
            return render(request, "courses.html", {"instructors": instructors, "tachoices": tachoices})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})

    def post(self, request):
        coursename = request.POST['name']
        instructorname = request.POST['instructorchoice']
        taname = request.POST['tachoice']
        desc = request.POST['description']

        if coursename == '' or instructorname == "Select..." or taname == "Select..." or desc == '':
            messages.error(request, 'Please fill all the boxes')
            return redirect('/courses/')

        instructorchoice = Instructor.objects.get(name=instructorname)
        tachoice = TA.objects.get(name=taname)

        user = MyUser.objects.get(name=request.session.get("name", False))

        Course.objects.create(name=coursename, description=desc, instructor=instructorchoice, instructorTA=tachoice)

        if direct(user.role) is not None:
            messages.success(request, "Success")
            return redirect(direct(user.role).url)
        else:
            return redirect("login.html", {"message": "unauthorized access"})


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
        return render(request, "login.html", {"message": "Success!"})


class EditCourse(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        if valid(user.role, "Admin"):
            courses = list(Course.objects.all())
            instructors = list(Instructor.objects.all())
            tachoices = list(TA.objects.all())

            jsoncourses = serializers.serialize('json', courses)
            jsoninstructors = serializers.serialize('json', instructors)
            jsontachoices = serializers.serialize('json', tachoices)
            return render(request, "editcourse.html",
                          {"courses": courses, "instructors": instructors, "tachoices": tachoices,
                           "jsoncourses": jsoncourses, "jsoninstructors": jsoninstructors,
                           "jsontachoices": jsontachoices})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})


class DeleteCourse(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)

        if valid(user.role, "Admin") or valid(user.role, "Instructor"):
            courses = list(map(str, Course.objects.all()))
            return render(request, "assign_TAs.html", {"courses": courses})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})

    def post(self, request):
        course = request.POST['coursechoice']

        if course == "Select...":
            messages.error(request, 'Please fill all the boxes')
            return redirect('/assign_TAs/')
        selectedCourse = Course.objects.get(course)
        user = MyUser.objects.get(name=request.session.get("name"))
        if direct(user.role) is not None:
            selectedCourse.delete()
            messages.success(request, 'Successfully assigned TA to Lab')
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})


class CreateTA(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        instructorchoice = list(Instructor.objects.all())
        if valid(user.role, "Admin") or valid(user.role, "Instructor"):
            return render(request, "TAs.html", {"instructors": instructorchoice})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})

    def post(self, request):
        taname = request.POST.get('name')
        instructorname = request.POST.get('instructorchoice')
        password = request.POST.get('password')

        if instructorname == "Select..." or taname == '' or password == '':
            messages.error(request, 'Please fill all the boxes')
            return redirect('/TAs/')

        if TA.objects.filter(name=taname).exists():
            messages.error(request, 'TA already exists')
            return redirect('/TAs/')

        MyUser.objects.create(name=taname, password=password, role="TA")
        TA.objects.create(name=taname, project_manager=Instructor.objects.get(name=instructorname))

        user = MyUser.objects.get(name=request.session.get("name", False))

        if direct(user.role) is not None:
            messages.success(request, 'Success')
            return redirect(direct(user.role).url)
        else:
            return redirect("login.html", {"message": "unauthorized access"})


class TA_home(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        lablist = list(Lab.objects.filter(labTA = TA.objects.get(name = loggedIn)))
        if valid(user.role, "TA"):
            return render(request, "TA_home.html", {'labs':lablist})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})


class Instructor_home(View):
    def get(self, request, ):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        if valid(user.role, "Instructor"):
            TAList = list(map(str, TA.objects.all()))
            InstructorList = list(map(str, Instructor.objects.all()))
            teacher = Instructor.objects.get(name=request.session.get("name", False))
            CourseList = list(Course.objects.filter(instructor=teacher))
            return render(request, "instructor_home.html",
                          {"TAs": TAList, "instructors": InstructorList, "courses": CourseList, "teacher": teacher})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})


class CreateInstructor(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)
        if valid(user.role, "Admin") or valid(user.role, "Instructor"):
            return render(request, "instructors.html", {})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})

    def post(self, request):
        loggedIn = request.session["name"]
        instructorname = request.POST.get('instructor')
        password = request.POST.get('password')

        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)

        if instructorname == '' or password == '':
            messages.error(request, 'Please fill all the boxes')
            return redirect('/instructors/')

        if Instructor.objects.filter(name=instructorname).exists():
            messages.error(request, 'Instructor already exists')
            return redirect('/instructors/')

        if not Administrator.objects.filter(name='Admin').exists():
            Administrator.objects.create(name="Admin", password="Admin")

        projManager = Administrator.objects.get(name="Admin")
        MyUser.objects.create(name=instructorname, password=password, role='Instructor')
        Instructor.objects.create(name=instructorname, project_manager=projManager)

        if direct(user.role) is not None:
            messages.success(request, 'Success')
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})


class Assign_TAs(View):
    def get(self, request):
        loggedIn = request.session.get("name")
        if MyUser.objects.filter(name=loggedIn).exists():
            user = MyUser.objects.get(name=loggedIn)

        if valid(user.role, "Admin") or valid(user.role, "Instructor"):
            courses = list(map(str, Course.objects.all()))
            tachoices = list(map(str, TA.objects.all()))
            return render(request, "assign_TAs.html", {"courses": courses, "tachoices": tachoices})
        else:
            return render(request, "login.html", {"message": "unauthorized access"})

    def post(self, request):
        course = request.POST['coursechoice']
        ta = request.POST['tachoice']
        labname = request.POST['lab']

        if course == "Select..." or labname == '' or ta == "Select...":
            messages.error(request, 'Please fill all the boxes')
            return redirect('/assign_TAs/')

        thislab = Lab.objects.create(name=labname, labTA=TA.objects.get(name=ta), labForCourse=Course.objects.get(name=course))

        user = MyUser.objects.get(name=request.session.get("name"))
        if direct(user.role) is not None:
            messages.success(request, 'Successfully assigned TA to Lab' )
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})


class Go_Back(View):
    def get(self, request):
        user = MyUser.objects.get(name=request.session.get("name"))
        if direct(user.role) is not None:
            return redirect(direct(user.role).url)
        else:
            return redirect('login.html', {"message": "unauthorized access"})
