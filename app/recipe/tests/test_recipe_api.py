from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe, Tag, Ingredient

from ..serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse("recipe:recipe-list")

def sample_tag(user, name="Default Tag Name"):
    """Create a new tag """
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name="Cucumber"):
    """Create a new ingredient"""
    return Ingredient.objects.create(user=user, name=name)

def get_detailed_url(recipe_id):
    """Return the url for every recipe id """
    # return the kind of url : /api/recipe/recipe_id
    return reverse("recipe:recipe-detail", args=[recipe_id])

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

    def test_view_recipe_detail(self):
        """Test viewing recipe detail view """

        recipe = sample_recipe(user=self.user)
        # with a many to many field we use the add function in order 
        # to add new objects in those fields
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = get_detailed_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
        

        
