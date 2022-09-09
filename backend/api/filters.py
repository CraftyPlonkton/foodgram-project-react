from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    author = NumberFilter(field_name='author__id')
    is_favorited = NumberFilter(method='get_favorite_recipes')
    is_in_shopping_cart = NumberFilter(method='get_shopping_cart')
    tags = CharFilter(method='get_tags')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags')

    def get_tags(self, queryset, name, value):
        tags = self.request.GET.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        return []

    def get_favorite_recipes(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorited_by__id=user.id)
        return queryset

    def get_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__id=user.id)
        return queryset
