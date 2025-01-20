from django.db import models

class Name(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

#Test