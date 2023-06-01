from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import UnicodeUsernameValidator


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Email')
    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Никнейм',
                                validators=(UnicodeUsernameValidator,))
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
