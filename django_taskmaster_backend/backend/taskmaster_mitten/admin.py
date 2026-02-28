from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):

# Register your models here.
list_display = ("title", "completed")
admin.site.register(Task, TaskAdmin)