import random

from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    gender = random.choice(User.Gender.choices)[0]

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)


class SocialAppFactory(DjangoModelFactory):
    provider = 'facebook'

    class Meta:
        model = SocialApp
        django_get_or_create = ('name',)
