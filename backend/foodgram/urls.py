from django.urls import include, path
from django.contrib import admin
# 2025-06-06T18:04:13.130880


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('shortener.urls')),
]
