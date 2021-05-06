from django.contrib import admin
from .models import MyUser, Administrator, Instructor, TA, Course, Lab
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Administrator)
admin.site.register(Instructor)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(Lab)
