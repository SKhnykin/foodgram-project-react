from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=150,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50,
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Ингредиент'
        verbose_name = 'ингредиенты'

    def __str__(self) -> str:
        return self.name
