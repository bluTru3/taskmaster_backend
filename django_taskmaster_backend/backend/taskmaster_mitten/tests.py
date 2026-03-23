from datetime import date, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from taskmaster_mitten.models import Task


class AuthAndTaskApiTests(APITestCase):
	def setUp(self):
		self.register_url = reverse("register")
		self.login_url = reverse("token_obtain_pair")
		self.tasks_url = reverse("task-list-create")

	def authenticate(self, username="alice", password="Password123!"):
		User.objects.create_user(
			username=username,
			email=f"{username}@example.com",
			password=password,
		)
		response = self.client.post(
			self.login_url,
			{"username": username, "password": password},
			format="json",
		)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

	def test_user_can_register(self):
		payload = {
			"username": "newuser",
			"email": "newuser@example.com",
			"password": "StrongPass123!",
			"password_confirm": "StrongPass123!",
		}
		response = self.client.post(self.register_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.filter(username="newuser").exists())

	def test_auth_required_for_tasks_list(self):
		response = self.client.get(self.tasks_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_user_can_create_task(self):
		self.authenticate()
		payload = {
			"title": "Write backend docs",
			"description": "Need clear setup and endpoint details.",
			"status": "todo",
			"due_date": (date.today() + timedelta(days=1)).isoformat(),
		}
		response = self.client.post(self.tasks_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Task.objects.count(), 1)

	def test_cannot_mark_done_without_proper_description(self):
		self.authenticate()
		payload = {
			"title": "Task",
			"description": "short",
			"status": "done",
		}
		response = self.client.post(self.tasks_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("description", response.data)

	def test_user_cannot_access_other_users_task(self):
		owner = User.objects.create_user(
			username="owner", email="owner@example.com", password="Password123!"
		)
		other = User.objects.create_user(
			username="other", email="other@example.com", password="Password123!"
		)
		task = Task.objects.create(
			owner=owner,
			title="Private",
			description="owner task only",
		)

		login = self.client.post(
			self.login_url,
			{"username": other.username, "password": "Password123!"},
			format="json",
		)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

		detail_url = reverse("task-detail", kwargs={"pk": task.pk})
		response = self.client.get(detail_url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
