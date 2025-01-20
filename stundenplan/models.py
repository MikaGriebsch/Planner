from django.db import models

class Name(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.short_name})"
    
class Class(models.Model):
    name = models.CharField(max_length=10)
    nr_of_students = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, through="Teached_Subjects")

    def __str__(self):
        return self.name

class Teached_Subjects(models.Model):
    klasse = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    