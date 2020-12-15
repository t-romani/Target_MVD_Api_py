from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from users.models import User
from users.tests.factories import UserFactory
import faker

class LoginTests(APITestCase):
    SIGN_IN_ERROR_MESSAGE = 'Unable to log in with provided credentials.'

    @classmethod
    def setUpClass(self):
        self.user = UserFactory()
        self.password = faker.Faker().password()
        self.user.set_password(self.password)
        self.user.save()
        self.sign_in_url = reverse('rest_login')

    def test_sign_in_success(self):
        data=({'email': self.user.email, 'password': self.password})
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)

    def test_sign_in_wrong_password(self):
        data=({'email': self.user.email, 'password': 'wrong_pass'})
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'] == [LoginTests.SIGN_IN_ERROR_MESSAGE])

    def test_sign_in_unexistant_email(self):
        data=({'email': 'another@email.com', 'password': 'wrong_pass'})
        response = self.client.post(self.sign_in_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'] == [LoginTests.SIGN_IN_ERROR_MESSAGE])

    def test_sign_out_success(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.post('/dj-rest-auth/logout/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('detail' in response.data)

    @classmethod
    def tearDownClass(self):
        self.user.delete()