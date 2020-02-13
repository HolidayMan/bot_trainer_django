from django.db import models


class TgUser(models.Model):
    tg_id = models.IntegerField()
    first_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return str(self.id)


class Project(models.Model):
    title = models.CharField(max_length=256, blank=True)
    manager_name = models.CharField(max_length=256, blank=True)
    goal = models.CharField(max_length=256, blank=True)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey("TgUser", on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=256)
    date_start = models.DateTimeField(blank=True)
    duration = models.IntegerField(blank=True)
    completed = models.BooleanField(default=False)
    project = models.ForeignKey("Project", related_name="tasks", on_delete=models.CASCADE)

    def __str__(self):
        return self.header


class Performer(models.Model):
    name = models.CharField(max_length=256)
    task = models.ForeignKey("Task", related_name="performers", on_delete=models.CASCADE)
    user = models.ForeignKey("TgUser", on_delete=models.CASCADE, related_name="performers")

    def __str__(self):
        return self.name
