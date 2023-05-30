from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UnicodeUsernameValidator


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True,
                                validators=(UnicodeUsernameValidator,))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
