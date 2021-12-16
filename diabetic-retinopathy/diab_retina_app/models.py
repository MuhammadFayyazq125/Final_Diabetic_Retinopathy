from enum import unique
from django.db import models


# Create your models here.
class drReport(models.Model):
    Dr_name = models.CharField(max_length=100)
    Patient_name = models.CharField(max_length=100)
    img = models.ImageField()
    result = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        return self.Patient_name