from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag
from users.models import CustomUser


class TagFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             queryset=Tag.objects.all(),
                                             to_field_name='slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset
