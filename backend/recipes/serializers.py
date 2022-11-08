import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Ingredient, Tag


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
            'pk', 'name', 'measurement_unit'
        )
