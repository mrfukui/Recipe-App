from django.test import TestCase

from .models import User

# Create your tests here.

class UserModelTest(TestCase):

  def setUpTestData():
    # Create an object
    User.objects.create(username='BigChungus')

  def test_user_name_length(self):
    user = User.objects.get(id=1)
    # Retrieve first object
    username_max_length = user._meta.get_field('username').max_length

    self.assertEqual(username_max_length, 36)

