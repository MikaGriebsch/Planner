from django.db import models
from django.core.exceptions import ValidationError

class Grade(models.Model):
    grade = models.IntegerField()
    def __str__(self):
        return f"{self.grade}"
    

class Subject(models.Model):
    abkuerzung = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    grade = models.ManyToManyField(Grade, through='Subject_Grade')
    def __str__(self):
        return f"{self.name} ({self.abkuerzung})"
    
    pass

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.short_name})"
    pass

class Class(models.Model):
    name = models.CharField(max_length=10)
    schueleranzahl = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, through='Teacher_Class')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=-1) #wenn ID==1 ist etwas falsch

    def __str__(self):
        return f"{self.name}"


class Teacher_Class(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    klasse = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def clean(self):
        if self.subject not in self.teacher.subjects.all():
            raise ValidationError(f"The subject {self.subject} is not taught by {self.teacher}")
        if Teacher_Class.objects.filter(teacher=self.teacher, klasse=self.klasse, subject=self.subject).exists(): 
            raise ValidationError(f"The teacher {self.teacher} already taugth {self.subject} in {self.klasse}")

class Subject_Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    wochenstunden = models.IntegerField()
    

class Lesson(models.Model):
    LESSON_NUMBER_CHOICES = [
        ('1', '1 Stunde'),
        ('2', '2 Stunde'),
        ('3/4', '3/4 Stunde'),
        ('5/6', '5/6 Stunde'),
        ('7/8', '7/8 Stunde'),
    ]
    lesson_number = models.TextField(
        choices=LESSON_NUMBER_CHOICES

    )

    WEEKDAY_CHOICES = [
        ('MO', 'Montag'),
        ('DI', 'Dienstag'),
        ('MI', 'Mittwoch'),
        ('DO', 'Donnerstag'),
        ('FR', 'Freitag'),
    ]

    weekday = models.CharField(
        max_length=2,
        choices=WEEKDAY_CHOICES,

    )

    def __str__(self):
        return self.weekday 
