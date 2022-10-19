from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import include, path

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
]
