from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.

def home(request):
  return render(request, 'recipes/welcome.html')

class RecipeListView(ListView):
  model = Recipe
  template_name = 'recipes/recipes_home.html'

class RecipeDetailView(DetailView):
  model = Recipe
  template_name = 'recipes/recipe_detail.html'

