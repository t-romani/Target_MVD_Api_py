from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')
        NOT_SPECIFIED = 'NS', ('Not specified')

    gender = models.CharField(max_length=2, choices=Gender.choices, default='NS')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
