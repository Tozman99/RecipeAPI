from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

# we'll make our test in order to check or create user 

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")
ME_URL = reverse("users:me") # url for our user data 

# use **params when a dict should be in a dict 
# use params when we need a dict 
def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)

# there is two kind of Api Test : Public Api tests and Private Api Tests
#1) Public Api tests means that your test is to create a user 
# Post request are public cause anyone can create a user 
# public request are: GET() and POST()
#2) Private Api Tests means test when the user update their account 
# this update are private to the specific user , PATCH() PUT()
class PublicUserApiTests(TestCase):
    """ Test the users API(Public) """

    def setUp(self):
        """Instantiate our APiclient """
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating using a valid paylof is successful"""

        payload = {
            'email': "letest@gmail.com",
            'password': "testpassword",
            'name': "Karim The S",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        # HTTP_201_CREATED = 201 = your post request has been succefulled
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        #check if our encrypted password = password of the user
        self.assertTrue(user.check_password(payload['password']))
        #check if the password of the user is not in the information
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""

        payload = {
            'email': "letest@gmail.com",
            'password': "testpassword",
            'name': "Karim The S",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test password must be more than 5 characters """
        
        payload = {
            'email': "letest@gmail.com",
            'password': "t",
            'name': "Lesoss",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists) # return True when user exist
    
    def test_create_token_for_user(self):
        """Test that token is created for the user"""

        payload = {"email":"egrgr@gmail.com", "password": "testpass"}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created of invalid credentials are given """

        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""

        payload = {"email":"x", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # in the public test we'll create tests to retrive an actual user

    def test_retrieve_user_unauthorized(self):
        """Test that authentification are required for users"""
        # this test should have a status of 401 = unauthorized request 
        # cause we don't want unauthenticated user to access other user data

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# now we'll create Private Tests 
# private tests are test that require authentification 
# it's related to users that are authenticated if they are autheticated 
# then they can edit their data


class PrivateUserApiTests(TestCase):
    """Test api requests that require authentification """

    def setUp(self):

        self.user = create_user(
                email="Karim@gmail.com", 
                name="Karim",
                password="testpass"
                        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
                "email": self.user.email,
                "name": self.user.name
                                        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on the me url """

        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user """
        # Payload is the new data that the user patched 
        # it means that payload are updated datas 
        payload = {"name": "newnameKarim", "password": "Testpassword1234$"}
        # we use the patch method from HTTP to edit existing ressources 
        # in this case the new user data are payload and it'll change the 
        # old user data we the patch method 
        # those old datas are located in the url (endpoint)
        # and with the URI(Unifrom ressource identifier), thoses data are
        # "patched" = edited for the specific ressource 
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db() # refresh the db in order to save edited datas

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check if the name of the user has been edited 
        self.assertEqual(self.user.name, payload["name"])
        # we check if the user password = the new password 
        self.assertTrue(self.user.check_password(payload["password"]))
