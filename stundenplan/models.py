from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.short_name})"
    pass

class Grade(models.Model):
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.grade}"
    
class Class(models.Model):
    name = models.CharField(max_length=10)
    schueleranzahl = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, through='Teached_Subject')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=-1) #wenn ID==1 ist etwas falsch

    def __str__(self):
        return f"{self.name} hat {self.schueleranzahl} Schüler"


class Subject(models.Model):
    abkuerzung = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.abkuerzung})"

class Teached_Subject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    klasse = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)


class Subject_Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    wochenstunden = models.IntegerField()