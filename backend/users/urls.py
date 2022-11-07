from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/<int:users_id>/subscribe/', FollowViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
]