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

def get_sentinel_user():
    return User.objects.get_or_create(
        username='deleted_usr',
        first_name='deleted',
        last_name='user'
    )[0]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        verbose_name="Автор рецепта",
        related_name="recipes"
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        error_messages={
            'unique': ("Рецепт с таким названием уже есть."),
        },
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное время приготовления 1 мин.'
            ),
            MaxValueValidator(
                32767,
                message='Максимальное время приготовления 32767 мин.'
            )
        ]
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name='Теги',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name

    def delete_image(self):
        self.image.delete()


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='get_ingredients')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='get_recipes')
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиентов не может быть меньше 1.'
            ),
            MaxValueValidator(
                32767,
                message='Количество ингредиентов не может быть больше 32767.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient_unique',
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.ingredient} в рецепте {self.recipe} - {self.amount} "
            f"{self.ingredient.measurement_unit}"
        )

class Favorite(models.Model):
    """ Избранное """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='favorite_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'