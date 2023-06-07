from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import TagFilter
from api.paginations import Paginate
from api.permissions import (IsAdminOrReadOnlyPermission,
                             IsAuthorOrReadOnlyPermission)
from api.serializers import (CustomUserSerializer, FavoriteSerializer,
                             IngredientSerializer, RecipeSerializer,
                             ShoppingCartSerializer, SubscriptionSerializer,
                             TagSerializer)
from api_foodgram.settings import (FONT_SIZE, X_CORD_TITLE, Y_CORD_TITLE,
                                   Y_REMOVAL)
from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
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

        serializer = SubscriptionSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

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
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self._add(FavoriteSerializer, request, pk)
        if request.method == 'DELETE':
            return self._delete(Favorite, request.user, pk)
        return None

    @action(methods=('post', 'delete'), detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self._add(ShoppingCartSerializer, request, pk)
        if request.method == 'DELETE':
            return self._delete(ShoppingCart, request.user, pk)
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
        pdf_create.setFont('94-font', FONT_SIZE)

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
        pdf_create.drawString(X_CORD_TITLE, Y_CORD_TITLE, 'Список покупок')
        x_cord = 100
        y_cord = 750
        for name, data in pdf_file.items():
            pdf_create.drawString(
                x_cord, y_cord, f'{name} - {data["amount"]} '
                f'{data["measurement_unit"]}'
            )
            y_cord -= Y_REMOVAL

        pdf_create.showPage()
        pdf_create.save()

        return response

    def _add(self, serializer, request, id):
        context = {"request": request}
        user = request.user.id
        recipe = get_object_or_404(
            Recipe.objects.add_user_annotations(user), id=id)
        data = {
            'user': user,
            'recipe': recipe.id
        }
        serializer = serializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete(self, model, user, id):
        obj = model.objects.filter(user=user, recipe__id=id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)
