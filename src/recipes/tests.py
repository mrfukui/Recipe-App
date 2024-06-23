from django.test import TestCase

from .models import Recipe

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

