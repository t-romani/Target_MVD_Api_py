import faker
from allauth.account.models import EmailAddress
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories import UserFactory
import faker


class LoginTests(APITestCase):
    SIGN_IN_ERROR_MESSAGE = 'Unable to log in with provided credentials.'
    EMAIL_NOT_VERIFIED = 'E-mail is not verified.'

    @classmethod
    def setUpClass(self):
        self.user = UserFactory()
        self.password = faker.Faker().password()
        self.user.set_password(self.password)
        self.user.save()
        EmailAddress(user_id=self.user.id, email=self.user.email, verified=True, primary=True).save()
        self.sign_in_url = reverse('rest_login')

    def test_sign_in_success(self):
        data = {'email': self.user.email, 'password': self.password}
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)

    def test_sign_in_wrong_password(self):
        data = {'email': self.user.email, 'password': 'wrong_pass'}
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'] == [LoginTests.SIGN_IN_ERROR_MESSAGE])

    def test_sign_in_unexistant_email(self):
        data = {'email': 'another@email.com', 'password': 'wrong_pass'}
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'] == [LoginTests.SIGN_IN_ERROR_MESSAGE])

    def test_sign_out_success(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.post(reverse('rest_logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('detail' in response.data)

    def test_login_without_confirmation(self):
        ea = EmailAddress.objects.get()
        ea.verified = False
        ea.save()
        data = {'email': self.user.email, 'password': self.password}
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'] == [LoginTests.EMAIL_NOT_VERIFIED])

    @classmethod
    def tearDownClass(self):
        self.user.delete()
