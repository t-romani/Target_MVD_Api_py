from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from users.models import User
from users.tests.factories import UserFactory
import factory

class SignUpTests(APITestCase):
  def setUp(self):
    self.data=factory.build(dict, FACTORY_CLASS=UserFactory)

  def test_sign_up_success(self):
    self.data.update({'password1': 'FairPass123', 'password2': 'FairPass123'})
    response = self.client.post('/dj-rest-auth/registration/', self.data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(User.objects.count(), 1)
    self.assertEqual(User.objects.get().first_name, self.data['first_name'])

  def test_sign_up_unmatched_passwords(self):
    self.data.update({'password1': 'FairPass123', 'password2': 'DifferentPass'})
    response = self.client.post('/dj-rest-auth/registration/', self.data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(User.objects.count(), 0)
    self.assertTrue(response.data['non_field_errors'] == ["The two password fields didn't match."])

