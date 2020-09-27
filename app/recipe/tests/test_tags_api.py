from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class TestPublicTagsApi(TestCase):
    """Test the public api of tags."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required to create a tag."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateTagsApi(TestCase):
    """Test the autherized user tags api."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@test.com',
            password='test1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags."""
        Tag.objects.create(user=self.user, name='TestTag',)
        Tag.objects.create(user=self.user, name='TestTag2')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authentication user."""
        user2 = get_user_model().objects.create_user(
            email='user2@test.com',
            password='test1234'
        )
        Tag.objects.create(
            user=user2,
            name='TestUser1'
        )
        tag = Tag.objects.create(
            user=self.user,
            name='TestUser2'
        )

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test successful creating and returning a tag."""
        payload = {'name': 'TestTag'}

        res = self.client.post(TAGS_URL, payload)

        exists_tag = Tag.objects.filter(
            user=self.user, name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists_tag)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload."""
        payload = {'name': ''}

        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
