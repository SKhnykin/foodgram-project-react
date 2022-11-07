from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователей.
    """
    CHOICES = (
        ('user', 'user'), ('admin', 'admin')
    )
    email = models.EmailField(
        'Email',
        max_length=200,
        blank=False,
        unique=True,)
    first_name = models.CharField(
        'Имя',
        blank=False,
        max_length=150)
    last_name = models.CharField(
        'Фамилия',
        blank=False,
        max_length=150)
    role = models.CharField(max_length=150, choices=CHOICES, default='user')
    password = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Пароль'
    )
    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Ник'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username}'


class Subscribe(models.Model):
    """
    Модель подписок
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')
    created = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'
