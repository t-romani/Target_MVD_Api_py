import factory
from factory import Faker
from factory.django import DjangoModelFactory

from targets.models import Topic


class TopicFactory(DjangoModelFactory):
    title = Faker('word')
    image = factory.django.ImageField(color='blue')

    class Meta:
        model = Topic
