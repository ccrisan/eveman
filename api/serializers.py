from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Event


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "first_name", "last_name")
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data["username"], validated_data["email"], validated_data["password"])
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.save()

        return user


class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("name", "description", "moment", "created_by", "max_attendees")
        read_only_fields = ("created_by",)


# We use the exact same fields for updating as for creating
UpdateEventSerializer = CreateEventSerializer


class ViewEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "name", "description", "moment", "created_by", "attendees", "max_attendees")
