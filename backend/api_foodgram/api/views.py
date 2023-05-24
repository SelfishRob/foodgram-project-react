from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeSerializer, TagSerializer)
from recipes.models import (Ingredient, Recipe,
                            Tag)
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
