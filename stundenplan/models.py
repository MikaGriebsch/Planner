from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model
from django.db.models.constraints import UniqueConstraint

class Grade(models.Model):
    name = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(12)])

    class Meta:
        verbose_name = 'Klassenstufe'
        verbose_name_plural = 'Klassenstufen'

    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    abkuerzung = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    grade = models.ManyToManyField(Grade, through='Subject_Grade')

    class Meta:
        verbose_name = 'Fach'
        verbose_name_plural = 'Fächer'

    def __str__(self):
        return f"{self.name} ({self.abkuerzung})"
    
    pass

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)
    subjects = models.ManyToManyField(Subject)

    class Meta:
        verbose_name = 'Lehrer'
        verbose_name_plural = 'Lehrer'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.short_name})"
    pass

class Class(models.Model):
    NAME_CHOICES = [
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('l', 'l')
    ]

    name = models.CharField(max_length=1, choices=NAME_CHOICES)
    schueleranzahl = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], default=30)
    schueler_in_class = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=0)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=-1)  # wenn ID==1 ist etwas falsch
    bezeichnung = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Klasse'
        verbose_name_plural = 'Klassen'

    def get_stundenplan(self):
        return Lesson.objects.filter(klasse=self).order_by('weekday', 'lesson_number')

    def save(self, *args, **kwargs):
        if not self.bezeichnung:
            self.bezeichnung = f"{self.grade.name}{self.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grade}{self.name}"

class Subject_Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    wochenstunden = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Klassenstufe-Fach'
        verbose_name_plural = 'Klassenstufe-Fach'

    def clean(self):
        if Subject_Grade.objects.filter(
            subject=self.subject,
            grade=self.grade
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Das Fach {self.subject} wird in diesem Jahrgang bereits unterrichtet."
            )

class Room(models.Model):
    room_number = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Raum'
        verbose_name_plural = 'Räume'

    def __str__(self):
        return f"{self.room_number}"

class Week(models.Model):
    WEEK_CHOICES = [
        ('A', 'A-Woche'),
        ('B', 'B-Woche'),
    ]
    week_choice = models.CharField(choices=WEEK_CHOICES, max_length=7, default='A')
    class Meta:
        verbose_name = 'Wochenoption'
        verbose_name_plural = 'Wochenoptionen'

    def __str__(self):
        return f"{self.week_choice}"

class Lesson(models.Model):
    LESSON_NUMBER_CHOICES = [
        ('1', '1 Stunde'),
        ('2', '2 Stunde'),
        ('3/4', '3/4 Stunde'),
        ('5/6', '5/6 Stunde'),
        ('7/8', '7/8 Stunde'),
    ]
    

    WEEKDAY_CHOICES = [
        ('MO', 'Montag'),
        ('DI', 'Dienstag'),
        ('MI', 'Mittwoch'),
        ('DO', 'Donnerstag'),
        ('FR', 'Freitag'),
    ]
    
    lesson_number = models.CharField(max_length=5, choices=LESSON_NUMBER_CHOICES, null=True)
    weekday = models.CharField(max_length=2, choices=WEEKDAY_CHOICES, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    klasse = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    week_choice = models.ForeignKey(Week, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['teacher', 'subject', 'klasse', 'weekday', 'lesson_number'], name='unique_lesson')
        ]
        verbose_name = 'Stunde'
        verbose_name_plural = 'Stunden'

    def clean(self):
        if Lesson.objects.filter(
            klasse=self.klasse,
            weekday=self.weekday,
            lesson_number=self.lesson_number,
            week_choice=self.week_choice,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Die Klasse {self.klasse} hat bereits ein Fach in der {self.lesson_number} Stunde ({self.week_choice}-Woche) am {self.weekday}."
            )

        if Lesson.objects.filter(
            teacher=self.teacher,
            weekday=self.weekday,
            lesson_number=self.lesson_number,
            week_choice=self.week_choice,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Der Lehrer {self.teacher} ist bereits in der {self.lesson_number} Stunde ({self.week_choice}-Woche) am {self.weekday} beschäftigt."
            )
        
        if Lesson.objects.filter(
            room_number=self.room_number,
            weekday=self.weekday,
            lesson_number=self.lesson_number,
            week_choice=self.week_choice,
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"Der Raum {self.room_number} ist bereits in der {self.lesson_number} Stunde ({self.week_choice}-Woche) am {self.weekday} in Benutzung."
            )

        if self.teacher and self.subject not in self.teacher.subjects.all():
            raise ValidationError(
                f"Der Lehrer {self.teacher} unterrichtet das Fach {self.subject} nicht."
            )
        
        if self.klasse.grade not in self.subject.grade.all():
            raise ValidationError(
                f"Das Fach {self.subject} wird in diesem Jahrgang nicht unterrichtet."
            )
        
        existing_lesson = Lesson.objects.filter(klasse=self.klasse, subject=self.subject).first()
        if existing_lesson and existing_lesson.teacher != self.teacher:
            raise ValidationError(
                f"Die Klasse {self.klasse} wird im Fach {self.subject} bereits von einem anderen Lehrer unterrichtet."
            )

    def __str__(self):
        return f"{self.weekday} - {self.lesson_number} - {self.klasse} ({self.subject})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    klasse = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    first_login = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Schüler Profile'
        verbose_name_plural = 'Schüler Profile'

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f"Profile von {self.user.username}"


class StundentDataImport(models.Model):
    name = models.CharField(max_length=50, default="Dateiname")
    file = models.FileField(upload_to="accounts/management/commands/tmp/")

    class Meta:
        verbose_name = 'Schülerliste Importieren '
        verbose_name_plural = 'Schülerlisten Importieren'

    def __str__(self):
        return self.name#
