from django.db.models import Q
from django.core.management.base import BaseCommand
from django.db import transaction
import csv
# 2025-06-06T18:04:13.130880
from django.conf import settings
# PEP8
from recipes.models import Tag




class Command(BaseCommand):
    help = 'Импортирует теги из CSV файла в базу данных'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'data/tags.csv'
        self.stdout.write(f'Чтение файла: {file_path}')

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
                            self.style.SUCCESS(
                                f'Успешно добавлено {len(tags_to_create)} тегов!'
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING('Нет новых тегов для добавления.')
                    )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {e}')
            )
