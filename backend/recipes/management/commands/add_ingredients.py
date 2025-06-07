from django.db import IntegrityError
from recipes.models import Ingredient
from django.conf import settings
from django.core.management.base import BaseCommand
import csv




class Command(BaseCommand):
    help = 'Импортирует ингредиенты из CSV файла в базу данных'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data/ingredients.csv'
        self.stdout.write(f'Чтение файла: {file_path}')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Пропускаем заголовок (если есть)  # noqa: F841

                ingredients_to_create = []
                for row in reader:
                    if len(row) < 2:
                        self.stdout.write(
                            self.style.WARNING(f'Пропущена некорректная строка: {row}')
                        )
                        continue

                    name, measurement_unit = row[0].strip(), row[1].strip()
                    if not name or not measurement_unit:
                        self.stdout.write(
                            self.style.WARNING(f'Пустое поле в строке: {row}')
                        )
                        continue

                    ingredients_to_create.append(
                        Ingredient(name=name, measurement_unit=measurement_unit)
                    )

                try:
                    Ingredient.objects.bulk_create(
                        ingredients_to_create,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Успешно добавлено {len(ingredients_to_create)} ингредиентов!')
                    )
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR('Ошибка: некоторые ингредиенты уже существуют.')
                    )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {e}')
            )
