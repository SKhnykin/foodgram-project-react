from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import HexColorValidator, TagSlugValidator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Ингредиент'
        verbose_name = 'ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        validators=[HexColorValidator(), ],
        unique=True
    )
    slug = models.CharField(
        'Уникальный slug',
        max_length=200,
        validators=[TagSlugValidator(), ],
        unique=True
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'
        constraints = [
            models.UniqueConstraint(fields=['name', 'slug'], name="Tag_unique")
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.slug}"
