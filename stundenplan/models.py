from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.constraints import UniqueConstraint

class Grade(models.Model):
    name = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(13)])
    def __str__(self):
        return f"{self.name}"
    

class Subject(models.Model):
    abkuerzung = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
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
    name = models.CharField(max_length=10, unique=True)
    schueleranzahl = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(40)])
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=-1) #wenn ID==1 ist etwas falsch

    def __str__(self):
        return f"{self.name}"

class Subject_Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    wochenstunden = models.IntegerField(validators=[MinValueValidator(1)])

    def clean(self):
        if Subject_Grade.objects.filter(
            subject=self.subject,
            grade=self.grade
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Das Fach {self.subject} wird bereits in diesem Jahrgang unterrichtet."
            )

class Room(models.Model):
    room_number = models.CharField(max_length=3, unique=True)
    def __str__(self):
        return f"{self.room_number}"

class Lesson(models.Model):
    LESSON_NUMBER_CHOICES = [
        ('1', '1 Stunde'),
        ('2', '2 Stunde'),
        ('3/4', '3/4 Stunde'),
        ('5/6', '5/6 Stunde'),
        ('7/8', '7/8 Stunde'),
    ]
    lesson_number = models.CharField(
        max_length=5,
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

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    klasse = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['teacher', 'subject', 'klasse', 'weekday', 'lesson_number'], name='unique_lesson')
        ]

    def clean(self):
        if Lesson.objects.filter(
            klasse=self.klasse,
            weekday=self.weekday,
            lesson_number=self.lesson_number
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Die Klasse {self.klasse} hat bereits ein Fach in der {self.lesson_number} Stunde am {self.weekday}."
            )

        if Lesson.objects.filter(
            teacher=self.teacher,
            weekday=self.weekday,
            lesson_number=self.lesson_number
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Der Lehrer {self.teacher} ist bereits in der {self.lesson_number} Stunde am {self.weekday} beschäftigt."
            )
        
        if Lesson.objects.filter(
            room_number=self.room_number,
            weekday=self.weekday,
            lesson_number=self.lesson_number
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Der Raum {self.room_number} ist bereits in der {self.lesson_number} Stunde am {self.weekday} in Benutzung."
            )

        if self.teacher and self.subject not in self.teacher.subjects.all():
            raise ValidationError(
                f"Der Lehrer {self.teacher} unterrichtet das Fach {self.subject} nicht."
            )
        
        if self.klasse.grade not in self.subject.grade.all():
            raise ValidationError(
                f"Das Fach {self.subject} wird in diesem Jahrgang nicht unterrichtet."
            )

    def __str__(self):
        return f"{self.weekday} - {self.lesson_number} - {self.klasse} ({self.subject})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    klasse = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile von {self.user.username}"