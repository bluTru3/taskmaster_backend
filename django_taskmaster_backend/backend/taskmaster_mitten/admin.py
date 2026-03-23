from django.contrib import admin
from taskmaster_mitten.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "status", "owner", "due_date", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("title", "description", "owner__username")