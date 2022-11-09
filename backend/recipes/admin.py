from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

EMPTY_MSG = '-пусто-'


class RecipeIngredientAdmin(admin.TabularInline):
    model = RecipeIngredient
    #autocomplete_fields = ('ingredients',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    list_display = (
        'name',
        'author',
        'cooking_time',
        'show_favorite_count'
    )

    def show_favorite_count(self, obj):
        """Счетчик добавления в избранное"""
        return obj.is_favorited.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = EMPTY_MSG


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    empty_value_display = EMPTY_MSG


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user'
    )


@admin.register(ShoppingCart)
class SoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_recipe', 'get_count')
    empty_value_display = EMPTY_MSG

    @admin.display(description='Рецепты')
    def get_recipe(self, obj):
        return [
            f'{item["name"]} ' for item in obj.recipe.values('name')[:5]]

    @admin.display(description='В избранных')
    def get_count(self, obj):
        return obj.recipe.count()
