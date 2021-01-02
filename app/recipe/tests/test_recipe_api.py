from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe

from ..serializers import RecipeSerializer


RECIPES_URL = reverse("recipe:recipe-list")

def sample_recipe(user, **params):
    """ Create a sample recipe """

    defaults = {
        "title": "Big Burger",
        "time_minutes": 10,
        "price": 5.00,
    }
    # with update the dict with other params such as the title 
    #this update method update value that as the same key for params 
    defaults.update(**params)
    # here we pass the dict in the recipe create fct 
    # this allows to put updated datas there 
    return Recipe.objects.create(user=user, **defaults)

class PublicRecipeTests(TestCase):
    """Test unauthenticated API Access"""

    def setUp(self):

        self.client = APIClient()
    
    def test_required_auth(self):
        """Test that we can't access the recipe when we aren't
        Authenticated"""

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "KarimS@gmail.com",
            "Testpass"
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_recipes(self):
        """Test that check if we get list recipe """
        # this sample recipe method return 
        # a recipe objects with default values 
        
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """ test if the user see only his recipe """
        
        user2 = get_user_model().objects.create_user(
            "Karimsetting@gmail.com",
            "Testpass"
        )
        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)


        
