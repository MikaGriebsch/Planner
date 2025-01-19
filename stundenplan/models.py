from django.db import models

class Lehrer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.short_name})"
