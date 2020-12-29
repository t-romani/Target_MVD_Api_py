import factory
import faker
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.tests.factories import UserFactory


class SignUpTests(APITestCase):
    PASSWORDS_UNMATCH = "The two password fields didn't match."
    ALREADY_REGISTERED = 'A user is already registered with this e-mail address.'
    SITE_NAME = 'example.com'

    def setUp(self):
        self.data = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.password = faker.Faker().password()

    def test_sign_up_success(self):
        self.data.update({'password1': self.password, 'password2': self.password})
        response = self.client.post('/dj-rest-auth/registration/', self.data)
        db_user = User.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(db_user.first_name, self.data['first_name'])
        self.assertEqual(db_user.last_name, self.data['last_name'])
        self.assertEqual(db_user.gender, self.data['gender'])

    def test_sign_up_unmatched_passwords(self):
        self.data.update({'password1': self.password, 'password2': 'DifferentPass'})
        response = self.client.post('/dj-rest-auth/registration/', self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['non_field_errors'], [SignUpTests.PASSWORDS_UNMATCH])

    def test_sign_up_email_already_exists(self):
        user = UserFactory()
        user.save()
        self.data.update({'email': user.email, 'password1': self.password, 'password2': self.password})
        response = self.client.post('/dj-rest-auth/registration/', self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], [SignUpTests.ALREADY_REGISTERED])

    def test_confirmation_email_sent(self):
        self.data.update({'password1': self.password, 'password2': self.password})
        self.client.post('/dj-rest-auth/registration/', self.data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [User.objects.get().email])
        self.assertEqual(mail.outbox[0].subject, f"[{SignUpTests.SITE_NAME}] Please Confirm Your E-mail Address")
