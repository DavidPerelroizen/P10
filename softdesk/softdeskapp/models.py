from django.db import models
from softdeskconf import settings

# Create your models here.


class Projects(models.Model):
    project_id = models.IntegerField()
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=3000)
    type = models.CharField()
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.Choices()
    role = models.CharField(max_length=30)


class Issues(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=3000)
    tag = models.CharField(max_length=10)
    priority = models.CharField(max_length=10)
    project_id = models.IntegerField()
    status = models.CharField(max_length=10)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=3000)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)

