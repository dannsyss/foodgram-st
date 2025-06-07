from django.urls import include, path
# Сделал импорты поприятнее
from .users.urls import user_router
# 2025-06-06T18:04:13.130880



app_name = 'api'

urlpatterns = [
    path('', include('api.recipes.urls')),
    path('', include(user_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
