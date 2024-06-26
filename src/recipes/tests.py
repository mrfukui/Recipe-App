from django.test import TestCase, Client
from .models import Recipe
from .forms import RecipesSearchForm
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class RecipeModelTest(TestCase):

  def setUpTestData():
    # Create an object
    Recipe.objects.create(name='Clam Chowder', ingredients='clams, potatoes, bacon, chicken stock', cooking_time=15, description='New England soup')

  def test_recipe_name(self):
    # Retrieve first object
    recipe = Recipe.objects.get(id=1)

    field_label = recipe._meta.get_field('name').verbose_name

    self.assertEqual(field_label, 'name')

  def test_recipe_cooking_time(self):

    recipe = Recipe.objects.get(id=1)

    cooking_time = recipe.cooking_time

    #Check to make sure cooking_time is an integer
    self.assertTrue(isinstance(cooking_time, int))
    # Check to make sure cooking_time is a positive integer
    self.assertGreater(cooking_time, 0)

  def test_get_absolute_url(self):
     
     recipe = Recipe.objects.get(id=1)

     self.assertEqual(recipe.get_absolute_url(), '/recipes/1')

  def test_difficulty_calculation(self):
     
     recipe = Recipe.objects.get(id=1)

     self.assertEqual(recipe.calculate_difficulty(), 'Hard')

class RecipeSearchTests(TestCase):

    def setUpTestData():
        # Create an object
        Recipe.objects.create(name='Clam Chowder', ingredients='clams, potatoes, bacon, chicken stock', cooking_time=15, description='New England soup')
        
    def test_search_form_valid(self):
        form_data = {'search_query': 'clams'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_invalid(self):
        form_data = {'search_query': ''}
        form = RecipesSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_difficulty_calculation(self):
        # Test the difficulty calculation method in the Recipe model
        recipe = Recipe.objects.get(name='Clam Chowder')
        self.assertEqual(recipe.calculate_difficulty(), 'Hard')
  
class SearchViewAccessTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.search_url = reverse('recipes:search')  # Replace with your actual URL name or pattern

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test recipe
        Recipe.objects.create(
            name='Clam Chowder',
            ingredients='clams, potatoes, bacon, chicken stock',
            cooking_time=15,
            description='New England soup'
        )

    def test_search_view_access_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the search view
        response = self.client.get(self.search_url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
