from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):

    def setUp(self):
        """User is authenticated"""

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "londondev@londonappdev.com", 
            "testpass"
            )
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags """
        # create two objects cause we want to test the list viewset 
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_tags_limited_to_user(self):
        """Test That tags returned are for authenticated user """
        # We want that a user authenticated is the only user that access is tags
        # if this user create a tag or another user then He should be the only
        # one to see the tag 
        # 
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_tag_successful(self):
        """Test that check if the tag has been created """

        #HTTP 405 status : https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405
        payload = {"name":"New Tag"}

        res = self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(user=self.user, name=payload["name"]).exists()
        self.assertTrue(exists)

    
    def test_create_tag_invalid(self):
        """Test that doen't create tag cause invalid name"""

        payload = {"name": ""}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
