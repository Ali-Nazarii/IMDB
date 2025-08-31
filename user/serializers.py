from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from rest_framework import serializers

if TYPE_CHECKING:
    from user.models import User as UserModel

User: "UserModel" = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
