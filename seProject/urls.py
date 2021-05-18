"""TAScheduler URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from TAApp import views
from TAApp.views import Assign_TAs, Login, Admin_home, Courses, Register, CreateTA, CreateInstructor, TA_home, \
    Instructor_home, EditCourse, Go_Back, DeleteCourse, makeassignment, thisCourse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('admin_home/', Admin_home.as_view(), name='admin_home'),
    path('courses/', Courses.as_view(), name='courses'),
    path('editcourse/', EditCourse.as_view(), name='edit_courses'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('TAs/', CreateTA.as_view(), name='create_TA'),
    path('TA_home/', TA_home.as_view(), name='TA_home'),
    path('instructors/', CreateInstructor.as_view(), name='create_instructor'),
    path('instructor_home/', Instructor_home.as_view(), name='instructor_home'),
    path('assign_TAs/', Assign_TAs.as_view(), name='assign_TA'),
    path('go_back/', Go_Back.as_view(), name='go_back'),
    path('deletecourse/', DeleteCourse.as_view(), name='delete_course'),
    path('createassignment/', makeassignment.as_view(), name='make_assignment'),
    path('thiscourse/', thisCourse.as_view(), name='this_course'),

]