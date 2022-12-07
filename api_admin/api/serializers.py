from rest_framework import serializers
from .models import Users

from django.db.models import fields

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'user_id',
            'firstname',
            'lastname',
            'email',
            'password',
            'role',
            'avatar',
            )