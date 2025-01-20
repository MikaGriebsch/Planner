from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)

class Grade(models.Model):
    grade = models.IntegerField()
    
class Class(models.Model):
    name = models.CharField(max_length=10)
    schueleranzahl = models.IntegerField()


class Subject(models.Model):
    abkuerzung = models.CharField(max_length=10)
    name = models.CharField(max_length=100)