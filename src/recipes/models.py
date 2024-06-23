from django.db import models
from django.shortcuts import reverse


# Create your models here.

class Recipe(models.Model):
    name=models.CharField(max_length=120)
    ingredients=models.CharField(max_length=500)
    cooking_time=models.PositiveIntegerField(help_text="in minutes")
    description=models.CharField(max_length=300)
    difficulty=models.CharField(max_length=15, default="TBD")
    pic=models.ImageField(upload_to="recipes", default="not-yet-image.png")

    def calculate_difficulty(self):
        
        num_ingredients = len(self.ingredients.split(', '))
        
        if self.cooking_time < 10 and num_ingredients < 4:
            difficulty = 'Easy'
        elif self.cooking_time < 10 and num_ingredients >= 4:
            difficulty = 'Medium'
        elif self.cooking_time >= 10 and num_ingredients < 4:
             difficulty = 'Intermediate'
        else:
            difficulty = 'Hard'
        return difficulty
    
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
       return reverse ('recipes:recipe_detail', kwargs={'pk': self.pk})