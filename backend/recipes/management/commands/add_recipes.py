from django.db import transaction
from django.core.management.base import BaseCommand
import random
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
# Не забыть поправить
from django.conf import settings
# Не забыть поправить
import json
from pathlib import Path
# PEP8
from django.contrib.auth import get_user_model
from django.core.files import File
# 2025-06-06T18:04:13.130880





User = get_user_model()


class Command(BaseCommand):
    help = 'Загружает рецепты из JSON файла'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data/recipes.json'
        image_path = settings.BASE_DIR / 'data/logo.png'  # Путь к изображению

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл не найден!'))
            return

        # Создаём тестового пользователя, если нет других
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING('Нет пользователей. Создаю тестового администратора...'))

            admin_user = User.objects.create_superuser(
                username='test_admin',
                email='admin@example.com',
                password='testpass123',
                first_name='Test',
                last_name='Admin'
            )
            users = [admin_user]

        author = random.choice(list(users))

        # Открываем изображение один раз
        try:
            image_file = open(image_path, 'rb')
            image = File(image_file, name=Path(image_path).name)
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('Изображение не найдено. Будет использовано пустое значение.'))
            image = None

        for recipe_data in data:
            self._create_recipe(recipe_data, author, image=image)

        if image and hasattr(image, 'closed') and not image.closed:
            image.close()

    def _create_recipe(self, recipe_data, author, image=None):
        tags = recipe_data.pop('tags', [])
        ingredients = recipe_data.pop('ingredients', [])
        recipe_name = recipe_data.get('name')

        if Recipe.objects.filter(name=recipe_name).exists():
            self.stdout.write(
                self.style.WARNING(f'Рецепт {recipe_name!r} уже существует.')
            )
            return

        try:
            with transaction.atomic():
                recipe = Recipe.objects.create(
                    author=author,
                    image=image,
                    **recipe_data
                )

                recipe_tags = Tag.objects.filter(slug__in=tags)
                recipe.tags.set(recipe_tags)

                for ingredient_data in ingredients:
                    ingredient_name = ingredient_data['name']
                    amount = ingredient_data['amount']

                    try:
                        ingredient = Ingredient.objects.get(name=ingredient_name)
                    except Ingredient.DoesNotExist:
                        raise ValueError(
                            f'Ингредиент {ingredient_name!r} не существует!'
                        )

                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount
                    )

                self.stdout.write(
                    self.style.SUCCESS(f'Успешно добавлен рецепт {recipe_name!r}')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при добавлении рецепта {recipe_name!r}: {e}')
            )
