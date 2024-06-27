from django.test import TestCase, Client
from .models import Recipe
from .forms import RecipesSearchForm, RecipeForm
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

class AddRecipeViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_add_recipe_get(self):
        # Test GET request to add_recipe view
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')
        self.assertIsInstance(response.context['form'], RecipeForm)

    def test_add_recipe_post_valid(self):
        # Test POST request with valid form data
        form_data = {
            'name': 'Test Recipe',
            'ingredients': 'Ingredient1, Ingredient2',
            'cooking_time': 30,
            'description': 'Test description',
            'pic': '',  # You may need to adjust this depending on your form handling
        }
        response = self.client.post(reverse('recipes:add_recipe'), data=form_data)
        
        # Check redirection to recipe_added page upon successful form submission
        self.assertRedirects(response, reverse('recipes:recipe_added'))
        
        # Verify that the recipe was created
        self.assertTrue(Recipe.objects.filter(name='Test Recipe').exists())

    def test_add_recipe_post_invalid(self):
        # Test POST request with invalid form data
        invalid_form_data = {
            # Missing required fields or invalid data
        }
        response = self.client.post(reverse('recipes:add_recipe'), data=invalid_form_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)