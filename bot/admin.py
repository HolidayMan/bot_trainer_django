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
    list_display = ("id", "title", "date_start", "duration", "performers")

    def performers(self, obj):
        return " ,".join(performer.name for performer in obj.performers.all())


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "task", "user")
