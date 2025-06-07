from django.utils.html import format_html
# PEP8
from django.contrib import admin
# PEP8
from recipes.models import (Recipe,
    Ingredient,
    Tag,
    RecipeIngredient,
    FavoriteRecipe,
    ShoppingCart,
)
from unfold.admin import ModelAdmin, TabularInline
from core.constants import INGREDIENT_MIN_AMOUNT




class IngredientsInRecipe(TabularInline):
    """Ингредиенты в рецепте — inline"""

    model = RecipeIngredient
    extra = 1
    min_num = INGREDIENT_MIN_AMOUNT


@admin.register(Recipe)
class RecipePanel(ModelAdmin):
    list_display = ("name", "author", "in_favorites")
    search_fields = ("name", "author__username", "author__email")
    search_help_text = "Поиск по названию, логину или email автора"
    filter_horizontal = ("tags",)
    list_filter = ("tags",)
    readonly_fields = ("in_favorites",)
    inlines = [IngredientsInRecipe]
    fieldsets = (
        (
            "Основные данные",
            {
                "fields": (
                    "author",
                    ("name", "cooking_time", "in_favorites"),
                    "text",
                    "image",
                    "tags",
                )
            },
        ),
    )

    @admin.display(description=format_html("<strong>Число в избранном</strong>"))
    def in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()


@admin.register(Tag)
class TagsPanel(ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name", "slug")
    search_fields = ("name", "slug")
    search_help_text = "Поиск по названию или слагу"


@admin.register(Ingredient)
class IngredientsPanel(ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_display_links = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию ингредиента"


@admin.register(FavoriteRecipe, ShoppingCart)
class UserRecipesPanel(ModelAdmin):
    list_display = ("id", "__str__")
    list_display_links = ("id", "__str__")
    search_fields = ("recipe__name", "user__username", "user__email")
    search_help_text = "Поиск по рецепту или пользователю"
