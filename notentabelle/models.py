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
    
    def average(self):
        notes = [
            self.note_1, self.note_2, self.note_3, self.note_4, self.note_5,
            self.note_6, self.note_7, self.note_8, self.note_9, self.note_10
        ]

        valid_notes = [note for note in notes if note is not None]
        if valid_notes:
            if self.klausur is not None:
                return round(sum(valid_notes) / len(valid_notes) * 0.75 + self.klausur * 0.25, 2)
            else:
                return round(sum(valid_notes) / len(valid_notes), 2)
            
        return None