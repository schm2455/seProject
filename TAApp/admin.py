from django.contrib import admin
from .models import MyUser, Administrator, Instructor, TA, Courses, Lab
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Administrator)
admin.site.register(Instructor)
admin.site.register(TA)
admin.site.register(Courses)
admin.site.register(Lab)