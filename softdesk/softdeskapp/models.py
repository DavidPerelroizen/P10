from django.db import models
from django.contrib.auth.models import User


# Create your models here.


CHOICES = (
    ('C','create'), ('Co', 'consult')
)


class Projects(models.Model):
    project_id = models.IntegerField()
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=3000)
    type = models.CharField(max_length=30)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.CharField(max_length=50, choices=CHOICES)
    role = models.CharField(max_length=30)


class Issues(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=3000)
    tag = models.CharField(max_length=10)
    priority = models.CharField(max_length=10)
    project_id = models.IntegerField()
    status = models.CharField(max_length=10)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=3000)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)

