from django_filters.rest_framework import (BooleanFilter,
    CharFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag





User = get_user_model()




class IngredientFilterSet(FilterSet):
    """
    Фильтр для модели Ингредиентов.
    Позволяет искать ингредиенты по частичному совпадению в начале названия.

    ⚠️ ВНИМАНИЕ:
    Сейчас фильтрация чувствительна к регистру (например, "Банан" ≠ "банан").
    Это может быть нежелательным поведением в боевом режиме.
    Для пользовательского интерфейса лучше использовать lookup_expr='istartswith'
    """

    name = CharFilter(
        field_name='name',
        lookup_expr='startswith',  # Теперь чувствителен к регистру
        label='Поиск по началу названия ингредиента (чувствителен к регистру)'
    )

    class Meta:
        model = Ingredient
        fields = {
            'name': ['exact', 'startswith'],  # Поддержка как точного совпадения, так и начала строки
        }


class RecipeFilterSet(FilterSet):
    """Фильтр для Рецептов"""

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(
        method='is_favorite_filter', field_name='favorites__author'
    )
    is_in_shopping_cart = BooleanFilter(
        method='is_in_shopping_cart_filter', field_name='shopping_cart__author'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def is_favorite_filter(self, queryset, name, value):
        return self.filter_from_kwargs(queryset, value, name)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return self.filter_from_kwargs(queryset, value, name)

    def filter_from_kwargs(self, queryset, value, name):
        if value and self.request.user.id:
            return queryset.filter(**{name: self.request.user})
        return queryset
