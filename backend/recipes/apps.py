from django.apps import AppConfig
# Сделал импорты поприятнее


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = 'Рецепты'
