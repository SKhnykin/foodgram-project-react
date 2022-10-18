from django.contrib import admin

from .models import Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('^name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
