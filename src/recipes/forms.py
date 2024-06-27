from django import forms    #import django forms
from .models import Recipe


class RecipesSearchForm(forms.Form):
    search_query = forms.CharField(label='Search for a recipe or ingredient for statistics', max_length=100)
    chart_type = forms.ChoiceField(
        choices=[
        ('#1', 'Bar chart'),    # when user selects "Bar chart", it is stored as "#1"
        ('#2', 'Pie chart'),
        ('#3', 'Line chart')
        ],
        required=False
    )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'description', 'pic']
        labels = {
            'name': 'Recipe Name',
            'ingredients': 'Ingredients (separated by a space and comma)',
            'cooking_time': 'Cooking Time',
            'description': 'Description',
            'pic': 'Recipe Image'
        }