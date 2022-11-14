from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from users.models import User, Subscribe

USER_ADD_SUBS = 'Пользователь уже добавлен в подписки'
ME_SUBS_NOT_EXISTS = 'Вы не подписаны на этого пользователя'
SUBSCRIBE_CANNOT_CREATE_TWICE = 'Нельзя подписаться дважды!'
SUBSCRIBE_CANNOT_CREATE_TO_YOURSELF = 'Нельзя подписаться на самого себя!'
SUBSCRIBE_CANNOT_DELETE = (
    'Нельзя отписаться от данного пользователя,'
    ' если вы не подписаны на него!'
)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Метод определяет подписан ли текущий пользователь на автора"""
        request = self.context.get('request')
        if request.user.is_anonymous or request is None:
            return False
        return Subscribe.objects.filter(user=request.user, author=obj).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserMeSerializer(serializers.ModelSerializer):
    """Эндпоинт /api/users/me/"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class RecipeShortSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для SubscribeSerializer"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeCreateSerializer(serializers.ModelSerializer):
    """Обрабатывает запросы на добавление/удаление из подписок"""

    def to_representation(self, value):
        """Отклик на POST запрос обрабатывается другим сериализатором"""
        return SubscribeSerializer(
            value.author,
            context={
                'request': self.context.get('request')
            }
        ).data

    def validate(self, data):
        request = self.context.get('request')
        user = self.context.get('request').user
        my_view = self.context['view']
        object_id = my_view.kwargs.get('users_id')
        if Subscribe.objects.filter(
            user=user,
            author=object_id
        ).exists() and request.method == 'POST':
            raise serializers.ValidationError({
                'errors': USER_ADD_SUBS})
        if not Subscribe.objects.filter(
            user=user,
            author=object_id
        ).exists() and request.method == 'DELETE':
            raise serializers.ValidationError({
                'errors': ME_SUBS_NOT_EXISTS})
        if (user.id == int(object_id)
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                SUBSCRIBE_CANNOT_CREATE_TO_YOURSELF
            )
        return data

    class Meta:
        model = Subscribe
        fields = '__all__'
        read_only_fields = (
            'user',
            'author'
        )


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit_recipes = request.query_params.get('recipes_limit')
        if limit_recipes:
            recipes = obj.recipe_author.all()[:(int(limit_recipes))]
        else:
            recipes = obj.recipe_author.all()
        context = {'request': request}
        return RecipeShortSerializer(recipes, many=True, context=context).data

    def get_recipes_count(self, obj):
        return obj.recipe_author.all().count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
