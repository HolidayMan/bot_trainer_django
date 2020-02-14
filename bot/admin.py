from django.contrib import admin
from .models import *


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_id", "first_name", "username", "date_joined")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_start", "date_end", "completed", "user")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_start", "duration", "display_performers")

    def display_performers(self, obj):
        return " ,".join(performer.name for performer in obj.performers.all())
    display_performers.short_description = "Related performers"


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "display_tasks", "project")

    def display_tasks(self, obj):
        return " ,".join(task.title for task in obj.tasks.all())

    display_tasks.short_description = "Related tasks"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project")