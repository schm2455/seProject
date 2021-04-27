from django.db import models


# Create your models here.


class MyUser(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Administrator(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=20)
    project_manager = models.ForeignKey(Administrator, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TA(models.Model):
    name = models.CharField(max_length=20)
    project_manager = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    project_manager = models.ForeignKey(Administrator, on_delete=models.CASCADE, null=True, blank=True, default="")
    instructor = models.ManyToManyField(Instructor)
    instructorTA = models.ManyToManyField(TA)


class Lab(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    project_manager = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True, default="")
    labTA = models.ManyToManyField(TA)
    labForCourse = models.ManyToManyField(Course)
