from django.contrib.auth import get_user_model
from django.db import models
from django.core import validators

User = get_user_model()


class Ingredient(models.Model):
    """
    Модель ингредиентов.
    """
    name = models.CharField(
        'Название ингредиента',
        blank=False,
        max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        blank=False,
        max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    """
    Модель тагов.
    """
    name = models.CharField(
        'Имя',
        max_length=60,
        unique=True)
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True)
    slug = models.SlugField(
        'Ссылка',
        max_length=100,
        unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient')
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Мин. количество ингридиентов 1'),),
        verbose_name='Количество',)

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']

    def __str__(self):
        return f'{self.ingredients}'


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name='Автор')
    name = models.CharField(
        'Название рецепта',
        max_length=255)
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='static/recipe/',
        blank=True,
        null=True)
    text = models.TextField(
        'Описание рецепта')
    cooking_time = models.BigIntegerField(
        'Время приготовления рецепта')
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        related_name='recipe_ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipe_tag')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Мин. время приготовления 1 минута'), ])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )
        verbose_name = 'recipe'

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class FavoriteRecipe(models.Model):
    """
    Модель избранных рецептов
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='is_favorited',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        unique_together = [['user', 'recipe']]

    def __str__(self):
        return f'{self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='is_in_shopping_cart'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        unique_together = [['user', 'recipe']]

    def __str__(self):
        return f'{self.recipe.name}'
