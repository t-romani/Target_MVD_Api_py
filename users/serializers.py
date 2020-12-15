# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from users.models import User


class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=User.Gender.choices)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.gender = self.data.get('gender')
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user
