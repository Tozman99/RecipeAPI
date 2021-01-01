from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models



def sample_user(email="karimS@gmail.com", password="testpass"):
    """ Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class UserModelTests(TestCase):

    def test_user_created_with_email(self):

        email = "xyz@gmail.com"
        password = "abcd1234"
        user = get_user_model().objects.create_user(
            email=email, 
            password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_created(self):
        """ Test for new user created with an email normalized """

        email = "fewf.kmkn@GMAIL.COM"
        user = get_user_model().objects.create_user(email=email, 
                                            password="vreb12")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test for invalid Email"""
        
        with self.assertRaises(ValueError):
            # email not provided if it raises a ValueError 
            # then the test pass
            get_user_model().objects.create_user(
                            email=None, password="geobbmr")

    def test_new_superuser(self):
        """Test for superuser Creation"""

        user = get_user_model().objects.create_superuser(
                                        email="frgrge@gmail.com", 
                                        password="rgegeg")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """ Test the tag string representation"""

        tag = models.Tag.objects.create(
            user = sample_user(),
            name="Vegan",
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test that the ingredient is a str """

        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test that the ingredient is a str """

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Hamburge with beef steak",
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

