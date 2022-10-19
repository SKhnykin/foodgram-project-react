from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from .validators import (NotDeletedUsernameValidator, NotMeUsernameValidator,
                         UsernameValidator)


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'), ('admin', 'admin')
    )
    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
        help_text=(
            "Введите username. "
            "Username может состоять из символов латинского "
            "алфавита [a-z A-Z], цифр [0-9] и спецсимволов: [ @ + - ]"
        ),
        validators=[
            NotMeUsernameValidator(),
            UsernameValidator(),
            NotDeletedUsernameValidator()
        ],
        error_messages={
            "unique": (
                "Пользователь с таким username уже есть, включите фантазию и "
                "придумайте другой username."
            ),
        },
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    role = models.CharField(max_length=150, choices=CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'


class Follow(models.Model):
    """
    Модель подписок\n
    Пользователь, который подписывается - user\n
    На кого подписывается - author
    """
    # Пользователь, который подписывается
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - кто подписан",
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - на кого подписан",
        related_name="following"
    )

    class Meta:
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "user"],
                name="Follow_unique"
            ),
        ]

    def __str__(self):
        return f"{self.user} follows {self.author}"