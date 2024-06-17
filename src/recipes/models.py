from django.db import models

# Create your models here.

class Recipe(models.Model):
  name=models.CharField(max_length=120)
  ingredients=models.CharField(max_length=500)
  cooking_time=models.PositiveIntegerField(help_text="in minutes")
  description=models.CharField(max_length=300)

  def __str__(self):
    return str(self.name)