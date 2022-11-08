from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, SubscribeViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/<int:users_id>/subscribe/', SubscribeViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
]