from . import views

from rest_framework import routers

from django.urls import include, path



router = routers.DefaultRouter()
router.register('tags', views.TagViewSet, 'tag')
router.register('recipes', views.RecipeViewSet, 'recipe')
router.register('ingredients', views.IngredientViewSet, 'ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
