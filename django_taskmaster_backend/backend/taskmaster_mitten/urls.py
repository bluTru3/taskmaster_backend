from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from taskmaster_mitten.views import (
    MeView,
    TaskDetailView,
    TaskListCreateView,
    UserRegisterView,
)

urlpatterns = [
    path("auth/register/", UserRegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
