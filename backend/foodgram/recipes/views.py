import os

from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.http import HttpResponse

from .paginators import RecipesCustomPagination
from .permissions import IsOwnerOrReadOnly

User = get_user_model()