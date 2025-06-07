from django.views.decorators.http import require_GET
# Сделал импорты поприятнее
from .models import LinkMapped

from django.http import HttpResponse
# Сделал импорты поприятнее
from django.shortcuts import get_object_or_404, redirect




@require_GET
def load_url(request, url_hash: str) -> HttpResponse:
    """Перенаправление с короткой ссылки на обычную"""
    original_url = get_object_or_404(
        LinkMapped, url_hash=url_hash
    ).original_url
    return redirect(original_url)
