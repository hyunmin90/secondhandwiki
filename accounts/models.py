from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0, blank=True, null=True)
    GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

