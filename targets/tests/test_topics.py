from django.core.files.storage import default_storage
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from targets.tests.factories import TopicFactory
from users.tests.factories import UserFactory


class TopicTests(APITestCase):
    AUTHENTICATION_ERROR_MESSAGE = 'Authentication credentials were not provided.'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.topic1 = TopicFactory()
        cls.topic2 = TopicFactory()
        cls.url = reverse('topics-list')
        cls.user = UserFactory()

    def test_list_topics_logged_in(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.topic1.title)
        self.assertEqual(response.data[0]['image'].split('?')[0], self.topic1.image.url.split('?')[0])
        self.assertEqual(response.data[1]['title'], self.topic2.title)
        self.assertEqual(response.data[1]['image'].split('?')[0], self.topic2.image.url.split('?')[0])

    def test_list_topics_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data['detail'] == TopicTests.AUTHENTICATION_ERROR_MESSAGE)

    def test_topic_image_name(self):
        self.assertEqual(self.topic1.image.name, self.topic1.title)

    @classmethod
    def tearDownClass(cls):
        default_storage.delete(cls.topic1.title)
        default_storage.delete(cls.topic2.title)
        super().tearDownClass()
