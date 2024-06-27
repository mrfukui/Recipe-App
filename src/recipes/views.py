from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipesSearchForm, RecipeForm
import pandas as pd
from .utils import get_recipename_from_id, get_chart
from django.db.models import Q

# Create your views here.

def home(request):
  return render(request, 'recipes/welcome.html')

class RecipeListView(LoginRequiredMixin, ListView):
  model = Recipe
  template_name = 'recipes/recipes_home.html'
  context_object_name = 'object_list'

  def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(ingredients__icontains=query)
            )
        return queryset

class RecipeDetailView(LoginRequiredMixin, DetailView):
  model = Recipe
  template_name = 'recipes/recipe_detail.html'

@login_required
def recipes_search(request):
    form = RecipesSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    search_list = None
    no_results = False

    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        chart_type = request.POST.get('chart_type')

        # Apply filter to search by recipe name or ingredients
        qs = Recipe.objects.filter(name__icontains=search_query) | Recipe.objects.filter(ingredients__icontains=search_query)
        search_list = Recipe.objects.filter(name__icontains=search_query) | Recipe.objects.filter(ingredients__icontains=search_query)
        
        if qs.exists():  # if data found
            recipes_df = pd.DataFrame(qs.values())
            recipes_df['recipe_id'] = recipes_df['id'].apply(get_recipename_from_id)
            y_label = "Cooking Time"
            chart = get_chart(chart_type, recipes_df, y_label=y_label, labels=recipes_df['name'].values)
            recipes_df = recipes_df.to_html()
        else:
            no_results = True

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
        'search_list': search_list,
        'no_results': no_results
    }

    return render(request, 'recipes/search.html', context)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes:recipe_added')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

@login_required
def recipe_added(request):
    return render(request, 'recipes/recipe_added.html')

@login_required
def about_me(request):
    return render(request, 'recipes/about_me.html')