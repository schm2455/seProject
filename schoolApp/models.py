from django.db import models

class MyUser(models.Model):
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)