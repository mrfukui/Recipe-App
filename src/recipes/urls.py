from django.urls import path
from .views import home, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
  path('', home),
  path('recipes/', RecipeListView.as_view(), name='recipe_list'),
  path('recipes/<pk>', RecipeDetailView.as_view(), name='recipe_detail')
]