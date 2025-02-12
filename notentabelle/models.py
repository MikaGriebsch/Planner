from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from stundenplan.models import Subject

class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    note_1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_3 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_4 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_5 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_6 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_7 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_8 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_9 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    note_10 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)
    klausur = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)], null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'subject'], name='unique_user_subject')
        ]
        verbose_name = 'Note'
        verbose_name_plural = 'Noten'

    def __str__(self):
        return f"{self.user.username}: {self.subject.name}"