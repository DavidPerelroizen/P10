from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()

    FIRST_NAME_FIELD = 'first_name'
    LAST_NAME_FIELD = 'last_name'
    EMAIL_FIELD = 'email'

