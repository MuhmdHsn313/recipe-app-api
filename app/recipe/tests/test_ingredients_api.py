from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


def simple_user(email='user@test.com', password='test1234'):
    """Create and returning a user"""
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
    )

    return user


INGREDIENT_URL = reverse('recipe:ingredient-list')


class TestPublicIngredientApi(TestCase):
    """Test public api of ingredient."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required to create an ingredient."""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_create_ingredents(self):
        """Test login is required to create a new ingredent."""
        payload = {'name': 'TestIngredent'}

        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateIngredientApi(TestCase):
    """Test private api of ingredient."""

    def setUp(self):
        self.user = simple_user()
        self.client = APIClient()

        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving all ingredients for user."""
        Ingredient.objects.create(
            user=self.user,
            name='TestIngredient'
        )
        Ingredient.objects.create(
            user=self.user,
            name='TestIngredient2'
        )

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingerdients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingerdients, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_retrieve_limited_user(self):
        """Test retrieve the ingredients for limited user."""
        user2 = simple_user(email='user2@test.com')
        Ingredient.objects.create(
            user=user2,
            name='TestIngredient'
        )
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='TestIngredient2'
        )

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_creating_successful_ingredient(self):
        """Test creating a new ingredient."""
        payload = {'name': 'TestIngredent'}

        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_ingredient(self):
        """Test create a new invalid ingredent."""
        payload = {'name': ''}

        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
