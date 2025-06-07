from . import views
from rest_framework import routers



user_router = routers.DefaultRouter()
user_router.register('users', views.UserViewSet, 'users')
