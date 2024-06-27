from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, recipes_search, add_recipe, recipe_added, about_me

app_name = 'recipes'

urlpatterns = [
  path('', home),
  path('recipes/', RecipeListView.as_view(), name='recipe_list'),
  path('recipes/<pk>', RecipeDetailView.as_view(), name='recipe_detail'),
  path('search/', recipes_search, name='search'),
  path('add/', add_recipe, name='add_recipe'),
  path('added/', recipe_added, name='recipe_added'),
  path('about/', about_me, name='about_me'),
]