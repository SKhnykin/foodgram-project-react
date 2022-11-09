from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteViewSet, IngredientViewSet, RecipeViewSet, ShoppingCartViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'recipes/<int:recipes_id>/shopping_cart/', ShoppingCartViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'recipes/<int:recipes_id>/favorite/', FavoriteViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        )
    )
]
