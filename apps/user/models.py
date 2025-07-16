from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
import random
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    is_active = models.BooleanField('Активный', default=True)
    code = models.IntegerField("Код активации", null=True, blank=True)
    email = models.EmailField('Эл-почта (логин)', unique=True)
    phone = models.IntegerField('Номер телефона', null=True, blank=True, unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='custom_user',
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = random.randint(100_000, 999_999)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('Имя', max_length=100, null=True, blank=True)
    email = models.EmailField('Эл-почта', null=True, blank=True)
    # is_active = models.BooleanField('Активный', default=True)


    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


