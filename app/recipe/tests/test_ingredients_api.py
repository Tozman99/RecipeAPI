from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient
from ..serializers import IngredientSerializer


INGREDIENTS_URL = reverse("recipe:ingredient-list")


class PublicIngredientApiTests(TestCase):
    """Test The publically available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint """

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the private availbale ingredients API, only for authenticated user"""

    def setUp(self):

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="KarimS@gmail.com",
            password="Testpass"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test for retreiving a list of ingredients"""

        Ingredient.objects.create(
            user=self.user,
            name="Cucumber"
        )

        Ingredient.objects.create(
            user=self.user,
            name="Apple"
        )

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for authenticated user are returned"""

        user_2 = get_user_model().objects.create_user(
            email="google@gmail.com",
            password="Testpass"
        )
        ingredient = Ingredient.objects.create(
            user=self.user,
            name="Cucumber"
        )
        Ingredient.objects.create(
            user=user_2,
            name="Apple"
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(len(res.data), 1)

    def test_create_ingredient_successful(self):
        """Test that an ingredient is created """

        payload = {"name": "Cucumber"}

        res = self.client.post(INGREDIENTS_URL, payload)
        exist = Ingredient.objects.filter(user=self.user, 
                                          name=payload["name"]).exists()
        
        self.assertTrue(exist)

    def test_create_ingredient_invalid(self):
        """Test Creating invalid ingredient"""

        payload = {"name": " "}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)





    