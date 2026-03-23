from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from taskmaster_mitten.models import Task


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password_confirm"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "owner",
            "created_at",
            "updated_at",
        ]


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "due_date"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value.strip()

    def validate(self, attrs):
        due_date = attrs.get("due_date")
        status = attrs.get("status", getattr(self.instance, "status", Task.Status.TODO))
        description = attrs.get("description", getattr(self.instance, "description", ""))

        if due_date and due_date < timezone.localdate() and status != Task.Status.DONE:
            raise serializers.ValidationError(
                {"due_date": "Due date cannot be in the past unless task is done."}
            )

        if status == Task.Status.DONE and len(description.strip()) < 10:
            raise serializers.ValidationError(
                {
                    "description": (
                        "Please add a meaningful description (10+ chars) before marking done."
                    )
                }
            )
        return attrs
