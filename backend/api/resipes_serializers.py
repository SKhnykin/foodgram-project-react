import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from .users_serializers import CustomUserSerializer

from recipes.models import (
    Ingredient,
    FavoriteRecipe,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)

RECIPES_NOT_FOUND = 'Рецепт не найден'
RECIPES_IN_LIST = 'Рецепт уже добавлен в список'
RECIPES_NOT_DELETED = 'Рецепт не находится в списке'


class TagSerializer(serializers.ModelSerializer):
    """Обрабатывает эндпоинт /api/tags/"""
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Обрабатывает эндпоинт /api/ingredients/"""
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для картинки"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Обрабатывает данные из 2ух моделей,
    к ингредиентам добавляет поле amount."""
    id = serializers.ReadOnlyField(source="ingredients.id")
    name = serializers.ReadOnlyField(source="ingredients.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredients.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Обрабатывает запросы на чтение на эндпоинт /api/recipes/"""
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(many=False, read_only=True)
    ingredients = RecipeIngredientSerializer(source='ingredient', many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Проверка на нахождение рецепта в избранных"""
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return FavoriteRecipe.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Если рецепт в списке покупок, вернет True"""
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    """Обрабатывает данные для 2ух моделей
    к ингредиентам добавляем поле amount. Используем для POST запросов
    на создание рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredients', queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Создание рецептов"""
    image = Base64ImageField(required=True, allow_null=True)
    tags = serializers.ListField(required=True)
    ingredients = CreateRecipeIngredientSerializer(required=True, many=True)

    def to_representation(self, value):
        """POST запрос обрабатываем другим сериализатором"""
        return RecipeSerializer(
            value,
            context={'request': self.context.get('request')}
        ).data

    def add_ingredients(self, ingredients_data, recipes):
        for ingredient in ingredients_data:
            current_ingredient, status = (
                RecipeIngredient.objects.get_or_create(**ingredient)
            )
            recipes.ingredients.add(current_ingredient)

    def create(self, validated_data):
        tag_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipes = Recipe.objects.create(**validated_data)
        recipes.tags.set(tag_data)
        self.add_ingredients(ingredients_data, recipes)
        return recipes

    def update(self, instance, validated_data):
        tag_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        recipes = instance
        recipes.tags.set(tag_data)
        recipes.ingredients.clear()
        self.add_ingredients(ingredients_data, recipes)
        return super().update(recipes, validated_data)


    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Обрабатываем эндпоинт /api/recipes/{id}/shopping_cart/"""
    main_model = ShoppingCart
    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        request = self.context.get('request')
        user = self.context.get('request').user
        my_view = self.context['view']
        object_id = my_view.kwargs.get('recipes_id')
        if not Recipe.objects.filter(id=object_id).exists():
            raise serializers.ValidationError({
                'errors': RECIPES_NOT_FOUND})
        if self.main_model.objects.filter(
            user=user,
            recipe=object_id
        ).exists() and request.method == 'POST':
            raise serializers.ValidationError({
                'errors': RECIPES_IN_LIST})
        if not self.main_model.objects.filter(
            user=user,
            recipe=object_id
        ).exists() and request.method == 'DELETE':
            raise serializers.ValidationError({
                'errors': RECIPES_NOT_DELETED})
        return data


class FavoriteRecipeSerializer(ShoppingCartSerializer):
    """Обрабатывает эндпоинт /api/recipes/{id}/favorite/"""
    main_model = FavoriteRecipe

    class Meta(ShoppingCartSerializer.Meta):
        model = FavoriteRecipe
