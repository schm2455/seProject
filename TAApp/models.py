from django.db import models

# Create your models here.


class MyUser(models.Model):
    name = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

class Administrator(models.Model):
    name = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=20, null=True)
    project_manager = models.ForeignKey(Administrator, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TA(models.Model):
    name = models.CharField(max_length=20, null=True)
    project_manager = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    project_manager = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True, blank=True, default="")
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    instructorTA = models.ForeignKey(TA, on_delete=models.CASCADE)

class Lab(models.Model):
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    project_manager = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True, default="")
    labTA = models.ForeignKey(TA, on_delete=models.CASCADE)
    labForCourse = models.ForeignKey(Course, on_delete=models.CASCADE)