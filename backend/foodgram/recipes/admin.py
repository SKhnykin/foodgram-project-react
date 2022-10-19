from django.contrib import admin

from .models import Favorite, Ingredient, Tag, Recipe, IngredientInRecipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class RecipeIngredientAdmin(admin.TabularInline):
    model = IngredientInRecipe
    fk_name = 'recipe'


# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('author', 'name', 'favorited')
#     list_filter = ('author', 'name', 'tags')
#     exclude = ('ingredients',)
#     search_fields = ('^name',)
#
#     inlines = [
#         RecipeIngredientAdmin,
#     ]
#
#     @admin.display(empty_value='Никто')
#     def favorited(self, obj):
#         return Favorite.objects.filter(recipe=obj).count()
#
#     favorited.short_description = 'Кол-во людей добавивших в избранное'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, RecipeIngredientAdmin)
