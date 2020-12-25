from django.test import TestCase
from django.contrib.auth import get_user_model


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
