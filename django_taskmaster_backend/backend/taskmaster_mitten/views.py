from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from taskmaster_mitten.models import Task
from taskmaster_mitten.permissions import IsOwner
from taskmaster_mitten.serializers import (
	TaskCreateUpdateSerializer,
	TaskListSerializer,
	UserRegisterSerializer,
)
from taskmaster_mitten.services import get_user_tasks


class UserRegisterView(generics.CreateAPIView):
	serializer_class = UserRegisterSerializer
	permission_classes = [permissions.AllowAny]


class MeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		user = request.user
		return Response(
			{
				"id": user.id,
				"username": user.username,
				"email": user.email,
			}
		)


class TaskListCreateView(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return get_user_tasks(self.request.user, self.request.query_params)

	def get_serializer_class(self):
		if self.request.method == "POST":
			return TaskCreateUpdateSerializer
		return TaskListSerializer

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [permissions.IsAuthenticated, IsOwner]

	def get_queryset(self):
		return Task.objects.all()

	def get_serializer_class(self):
		if self.request.method in ("PUT", "PATCH"):
			return TaskCreateUpdateSerializer
		return TaskListSerializer
