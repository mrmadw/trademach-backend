from rest_framework import serializers
from .models import NewUser


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NewUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "is_verified",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
            "password"
        ]
        read_only_fields = [
            "is_verified",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = NewUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
