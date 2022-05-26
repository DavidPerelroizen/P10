from django.db import models
from django.contrib.auth.models import User


# Create your models here.


CHOICES_ROLE = (
    ('A', 'author'),
    ('CONTR', 'contributor')
)

CHOICES_PERMISSION = (
    ('C', 'CRUD'), ('R', 'READ')
)

CHOICES_TYPE = (
    ('BE', 'back-end'),
    ('FE', 'front-end'),
    ('IOS', 'ios'),
    ('AN', 'android')
)

CHOICES_PRIORITY = (
    ('L', 'low'),
    ('M', 'medium'),
    ('H', 'high')
)

CHOICES_TAG = (
    ('B', 'bug'),
    ('I', 'improvement'),
    ('T', 'task')
)

CHOICES_STATUS = (
    ('T', 'to do'),
    ('I', 'in progress'),
    ('F', 'finished')
)


class Projects(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=3000)
    type = models.CharField(max_length=30, choices=CHOICES_TYPE)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')


class Contributors(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(max_length=50, choices=CHOICES_PERMISSION)
    role = models.CharField(max_length=30, choices=CHOICES_ROLE)


class Issues(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=3000)
    tag = models.CharField(max_length=20, choices=CHOICES_TAG)
    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=10, choices=CHOICES_STATUS)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=3000)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE, related_name='comments')
