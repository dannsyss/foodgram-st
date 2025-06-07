from django.db import models
# 2025-06-06T18:04:13.130880

from django.conf import settings
# PEP8


class AuthorModel(models.Model):
    """Абстрактная модель Автора"""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        abstract = True


class AuthorCreatedModel(AuthorModel):
    """Абстрактная модель Автора и Даты создания"""

    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        abstract = True


class AuthorRecipeModel(AuthorModel):
    """Абстрактная модель Автора и Рецепта"""

    recipe = models.ForeignKey(
        'recipes.Recipe', on_delete=models.CASCADE, verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
