from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from api.filters import TagFilter
from api.paginations import Paginate
from api.permissions import (IsAdminOrReadOnlyPermission,
                             IsAuthorOrReadOnlyPermission)
from api.serializers import (CustomUserSerializer,
                             IngredientSerializer,
                             RecipeMinifiedSerializer,
                             RecipeSerializer,
                             SubscriptionSerializer,
                             TagSerializer,)
from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag,)
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=('get',), detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        follow = Follow.objects.filter(user=user)
        paginator = Paginate()
        page = paginator.paginate_queryset(follow, request)
        serializer = SubscriptionSerializer(page, many=True,
                                            context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @action(methods=('post',), detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)

        if user == author:
            return Response({
                'errors': 'Нельзя подписываться на себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного автора'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, author=author)
        serializer = SubscriptionSerializer(follow,
                                            context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        follow = Follow.objects.filter(user=user, author=author)

        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Вы не подписаны на данного автора'
        }, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnlyPermission,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, id=None):
        if request.method == 'POST':
            return self._add(Favorite, request.user, id)
        elif request.method == 'DELETE':
            return self._delete(Favorite, request.user, id)
        return None

    @action(methods=('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, id=None):
        if request.method == 'POST':
            return self._add(ShoppingCart, request.user, id)
        elif request.method == 'DELETE':
            return self._delete(ShoppingCart, request.user, id)
        return None

    @action(methods=('get',), detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )

        # Добавление шрифта с поддержкой русского языка
        font_path = 'fonts/94-font.ttf'
        pdfmetrics.registerFont(TTFont('94-font', font_path))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"'
        )

        pdf_create = canvas.Canvas(response)
        pdf_create.setFont("94-font", 12)

        pdf_file = dict()
        for ingredient in ingredients:
            name = ingredient[0]
            if name not in pdf_file:
                pdf_file[name] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2]
                }
            else:
                pdf_file[name]['amount'] += ingredient[2]

        # Вывод списка покупок
        pdf_create.drawString(250, 800, 'Список покупок')
        y_cord = 750
        for name, data in pdf_file.items():
            pdf_create.drawString(
                100, y_cord, f'{name} - {data["amount"]} '
                f'{data["measurement_unit"]}'
            )
            y_cord -= 20

        pdf_create.showPage()
        pdf_create.save()

        return response

    def _add(self, model, user, id):
        if model.objects.filter(user=user, recipe__id=id).exists():
            return Response({
                'errors': 'Ошибка добавления рецепта'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(
            Recipe.objects.add_user_annotations(user.id), id=id)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeMinifiedSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete(self, model, user, id):
        obj = model.objects.filter(user=user, recipe__id=id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)
