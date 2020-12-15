from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from users.models import User
from users.tests.factories import UserFactory

class LoginTests(APITestCase):
  def setUp(self):
    self.user = UserFactory()
    self.password = 'FairPass123'
    self.user.set_password(self.password)
    self.user.save()

  def test_sign_in_success(self):
    data=({'email': self.user.email, 'password': self.password})
    response = self.client.post('/dj-rest-auth/login/', data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue('key' in response.data)

  def test_sign_in_wrong_password(self):
    data=({'email': self.user.email, 'password': 'wrong_pass'})
    response = self.client.post('/dj-rest-auth/login/', data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertTrue(response.data['non_field_errors'] == ['Unable to log in with provided credentials.'])

  def test_sign_in_unexistant_email(self):
    data=({'email': 'another@email.com', 'password': 'wrong_pass'})
    response = self.client.post('/dj-rest-auth/login/', data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertTrue(response.data['non_field_errors'] == ['Unable to log in with provided credentials.'])

  def test_sign_out_success(self):
    self.client.login(email=self.user.email, password=self.password)
    response = self.client.post('/dj-rest-auth/logout/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue('detail' in response.data)
