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
    
    def test_create_basic_recipe(self):
        """Test creating recipe"""
        # we check if our object created is legit cause we check if payload has the same attr/key
        # as the Recipe model 

        payload = {
            'title': 'Test recipe',
            'time_minutes': 30,
            'price': 10.00,
        }
        res = self.client.post(RECIPES_URL, payload)

        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'title': 'Test recipe with two tags',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 10.00
        }
        res = self.client.post(RECIPES_URL, payload)

        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_create_recipe_with_ingredients(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Ingredient 1')
        ingredient2 = sample_ingredient(user=self.user, name='Ingredient 2')
        payload = {
            'title': 'Test recipe with ingredients',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 45,
            'price': 15.00
        }

        res = self.client.post(RECIPES_URL, payload)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_partial_update_recipe(self):
        """Test updating a recipe with patch """
        # this'll test if we can modify partially a recipe object 

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name="Vegan")

        payload = {
            "title":"Best salad",
            "tags": [new_tag.id]
        }
        detailed_url = get_detailed_url(recipe.id)
        res = self.client.patch(detailed_url, payload)
        #https://docs.djangoproject.com/en/3.1/ref/models/instances/#refreshing-objects-from-database
        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload["title"])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        # with the put method we update the full object 
        # so if we don't provide some fields then there are considered as blank
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))

        payload = {
                'title': 'Spaghetti',
                'time_minutes': 25,
                'price': 5.00
        }
        url = get_detailed_url(recipe.id)
        self.client.put(url, payload)
        # we don't provide ingredients and tags so they are empty list
        
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
        # we chekck that tags are empty  cause we haven't provided this field in the payload 
        
        
