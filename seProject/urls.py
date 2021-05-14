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
    Instructor_home, EditCourse, Go_Back

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('admin_home/', Admin_home.as_view(), name='admin_home'),
    path('courses/', Courses.as_view()),
    path('editcourse/', EditCourse.as_view()),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('TAs/', CreateTA.as_view()),
    path('TA_home/', TA_home.as_view()),
    path('instructors/', CreateInstructor.as_view()),
    path('instructor_home/', Instructor_home.as_view()),
    path('assign_TAs/', Assign_TAs.as_view()),
    path('go_back/', Go_Back.as_view()),
]