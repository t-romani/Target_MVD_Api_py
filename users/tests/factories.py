import random
from factory import Faker
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from users.models import User, GENDER_SELECTION

class UserFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    gender = random.choice(GENDER_SELECTION)[0]

    class Meta:
      model = get_user_model()
      django_get_or_create = ('email',)
