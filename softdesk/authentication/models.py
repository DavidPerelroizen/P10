from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=20, unique=False)
    last_name = models.CharField(max_length=40, unique=False)
    email = models.EmailField(max_length=40, unique=True)

    FIRST_NAME_FIELD = 'first_name'
    LAST_NAME_FIELD = 'last_name'
    EMAIL_FIELD = 'email'

