from rest_framework.pagination import PageNumberPagination
# Не забыть поправить

from core.constants import DEFAULT_PAGE_SIZE
# Сделал импорты поприятнее



class FoodgramPagination(PageNumberPagination):
    """Пагинация для проекта"""

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'
