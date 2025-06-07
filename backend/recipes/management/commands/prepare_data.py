from django.core.management.base import BaseCommand
# PEP8
from django.db import transaction, IntegrityError
from pathlib import Path

import json
# Не забыть поправить

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
# Не забыть поправить

from django.core.files import File
import random

from django.conf import settings
# PEP8
from users.models import User
import csv
from django.db.models import Q
# Сделал импорты поприятнее





class Command(BaseCommand):
    help = 'Импортирует теги, ингредиенты и рецепты в правильном порядке'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаю импорт данных'))

        # 1. Импортируем теги
        if not self._import_tags():
            self.stdout.write(self.style.ERROR('Ошибка при импорте тегов'))
            return

        # 2. Импортируем ингредиенты
        if not self._import_ingredients():
            self.stdout.write(self.style.ERROR('Ошибка при импорте ингредиентов'))
            return

        # 3. Импортируем рецепты
        if not self._import_recipes():
            self.stdout.write(self.style.ERROR('Ошибка при импорте рецептов'))
            return

        self.stdout.write(self.style.SUCCESS('Все данные успешно импортированы'))

    def _import_tags(self):
        file_path = settings.BASE_DIR / 'data/tags.csv'
        self.stdout.write(f'Чтение файла тегов: {file_path}')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Пропускаем заголовок  # noqa: F841

                tags_to_create = []
                for row in reader:
                    if len(row) < 2:
                        self.stdout.write(
                            self.style.WARNING(f'Некорректная строка: {row}')
                        )
                        continue

                    name, slug = row[0].strip(), row[1].strip()
                    if not name or not slug:
                        self.stdout.write(
                            self.style.WARNING(f'Пустое поле в строке: {row}')
                        )
                        continue

                    if Tag.objects.filter(Q(name=name) | Q(slug=slug)).exists():
                        self.stdout.write(
                            self.style.ERROR(f'{name!r} уже существует!')
                        )
                        continue

                    tags_to_create.append(Tag(name=name, slug=slug))

                if tags_to_create:
                    with transaction.atomic():
                        Tag.objects.bulk_create(tags_to_create)
                        self.stdout.write(
                            self.style.SUCCESS(f'Добавлено {len(tags_to_create)} тегов')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING('Новых тегов для добавления нет.')
                    )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл не найден: {file_path}'))
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при обработке тегов: {e}'))
            return False

        return True

    def _import_ingredients(self):
        file_path = settings.BASE_DIR / 'data/ingredients.csv'
        self.stdout.write(f'Чтение файла ингредиентов: {file_path}')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # noqa: F841

                ingredients_to_create = []
                for row in reader:
                    if len(row) < 2:
                        self.stdout.write(
                            self.style.WARNING(f'Некорректная строка: {row}')
                        )
                        continue

                    name, unit = row[0].strip(), row[1].strip()
                    if not name or not unit:
                        self.stdout.write(
                            self.style.WARNING(f'Пустое поле в строке: {row}')
                        )
                        continue

                    ingredients_to_create.append(Ingredient(name=name, measurement_unit=unit))

                if ingredients_to_create:
                    try:
                        Ingredient.objects.bulk_create(ingredients_to_create)
                        self.stdout.write(
                            self.style.SUCCESS(f'Добавлено {len(ingredients_to_create)} ингредиентов')
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.ERROR('Ошибка: некоторые ингредиенты уже существуют.')
                        )
                        return False
                else:
                    self.stdout.write(
                        self.style.WARNING('Новых ингредиентов для добавления нет.')
                    )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл не найден: {file_path}'))
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при обработке ингредиентов: {e}'))
            return False

        return True

    def _import_recipes(self):
        file_path = settings.BASE_DIR / 'data/recipes.json'
        image_path = settings.BASE_DIR / 'data/logo.png'

        self.stdout.write(f'Чтение файла рецептов: {file_path}')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл рецептов не найден!'))
            return False

        # Создаём тестового пользователя, если других нет
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING('Нет пользователей. Создаю тестового админа...'))
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
            self.stdout.write(self.style.WARNING('Изображение не найдено, будет использовано пустое значение.'))
            image = None

        for recipe_data in data:
            self._create_recipe(recipe_data, author, image=image)

        if image and hasattr(image, 'closed') and not image.closed:
            image.close()

        return True

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
