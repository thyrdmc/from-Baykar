from rest_framework import serializers

from .models import *
from django.contrib.auth.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ['id','username', 'first_name', 'last_name']