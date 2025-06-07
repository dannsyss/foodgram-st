from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт тестового пользователя с правами администратора'

    def handle(self, *args, **options):
        email = 'dansys@mail.ru'
        username = 'Den_Sys'
        first_name = 'Den'
        last_name = 'Sys'
        password = '12345'

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Пользователь с email {email} уже существует.')
            )
            return

        try:
            admin_user = User.objects.create_superuser(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Тестовый админ создан: {admin_user.email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании пользователя: {e}')
            )
