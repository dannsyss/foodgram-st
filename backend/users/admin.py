from rest_framework.authtoken.models import TokenProxy

from .models import Subscriber, User
from unfold.admin import ModelAdmin

from django.contrib import admin
from django.contrib.auth.models import Group, User
from unfold.decorators import display
# Сделал импорты поприятнее


@admin.register(User)
class UserAdmin(ModelAdmin):
    """Админка пользователя с поддержкой Unfold"""

    list_display = ('id', 'full_name', 'username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    search_help_text = 'Поиск по `username` и `email`'
    list_display_links = ('id', 'username', 'email', 'full_name')

    @display(description='Имя фамилия')
    def full_name(self, obj):
        return obj.get_full_name()


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    """Подписки пользователей — отображение в админке"""

    list_display = ('id', 'user', 'author')
    list_display_links = ('id', 'user', 'author')
    search_fields = ('user__username', 'author__username')
    search_help_text = 'Поиск по имени подписчика или автора'


# Отключаем ненужные модели
admin.site.unregister([Group, TokenProxy])
