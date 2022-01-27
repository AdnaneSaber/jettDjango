from rest_framework import serializers
from .models import Model
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"
        depth = 1
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserCreateSerializerPatch(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['ppic']
