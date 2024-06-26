from django import forms    #import django forms


class RecipesSearchForm(forms.Form):
    search_query = forms.CharField(label='Search for a recipe or ingredient', max_length=100)
    chart_type = forms.ChoiceField(
        choices=[
        ('#1', 'Bar chart'),    # when user selects "Bar chart", it is stored as "#1"
        ('#2', 'Pie chart'),
        ('#3', 'Line chart')
        ],
        required=False
    )