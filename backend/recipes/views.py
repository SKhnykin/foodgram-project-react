from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.pagination import LimitPageNumberPagination
from users.permissions import OwnerOrReadOnly

from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)
from .serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    CreateRecipeSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from .filters import IngredientFilter, RecipeFilter

HEADING_SHOPING_LIST = 'Список покупок для приготовления:\n\n'


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def download_shopping_cart(request):
    """Формирует и отдает список покупок"""
    ingredients = RecipeIngredient.objects.filter(
        recipe_ingredients__is_in_shopping_cart__user=request.user
    )
    shopping_dict = {}
    data = HEADING_SHOPING_LIST
    for ingredient in ingredients:
        amount = ingredient.amount
        name = ingredient.ingredients.name
        measurement_unit = ingredient.ingredients.measurement_unit
        if name not in shopping_dict:
            shopping_dict[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
        else:
            shopping_dict[name]['amount'] += amount
    for ingredient in shopping_dict:
        data += ingredient + ' - ' + str(
            shopping_dict[ingredient]['amount']
        ) + ' ' + shopping_dict[ingredient]['measurement_unit'] + '\n'
    return HttpResponse(data, content_type='text/plain')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = LimitPageNumberPagination
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Обработка запросов на добавление/удаление из списка покупок"""
    serializer_class = ShoppingCartSerializer
    main_model = ShoppingCart
    queryset = main_model.objects.all()
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipes_id'))
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, recipes_id):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = self.main_model.objects.filter(
            recipe=recipes_id, user=request.user
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(ShoppingCartViewSet):
    """Обработка запросов на добавление/удаление из списка избранных"""
    serializer_class = FavoriteRecipeSerializer
    main_model = FavoriteRecipe
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)
