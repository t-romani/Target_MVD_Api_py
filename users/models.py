from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_SELECTION = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('NS', 'Not Specified'),
]

class User(AbstractUser):
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
