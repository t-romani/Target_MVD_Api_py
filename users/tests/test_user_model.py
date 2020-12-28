import random

import faker
from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.fake = faker.Faker()
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.email = self.fake.email()
        self.gender = random.choice(User.Gender.choices)[0]

        User.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            gender=self.gender,
        )

    def test_user_attributes(self):
        user = User.objects.get(email=self.email)

        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.gender, self.gender)
