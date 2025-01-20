from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)
    pass

class Grade(models.Model):
    grade = models.IntegerField()
    
class Class(models.Model):
    name = models.CharField(max_length=10)
    schueleranzahl = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, through='Teached_Subject')


class Subject(models.Model):
    abkuerzung = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class Teached_Subject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    klasse = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)