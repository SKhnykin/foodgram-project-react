from django.contrib import admin
# from django.contrib.auth import get_user_model

from .models import User, Subscribe
# User = get_user_model()
EMPTY_MSG = '-пусто-'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created',)
    search_fields = ('user__email', 'author__email',)
    empty_value_display = EMPTY_MSG
