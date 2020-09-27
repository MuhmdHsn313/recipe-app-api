from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def simple_user(email='user@test.com', password='test1234'):
    """Create and return a new simple user."""
    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )
    return user


class TestUserModel(TestCase):

    def test_user_creating_with_email(self):
        """Test Creating user with an email address."""
        email = 'test@gmail.com'
        password = '1234abcd'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_creating_user_normalize(self):
        """Test Creating a normalize email address for a new user."""
        email = 'test@GMAIL.COM'
        password = '1234abcd'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_creating_user_invalide_user_email(self):
        """Test raised a new ValueError when creating user with no email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='1234abcd'
            )

    def test_creating_superuser(self):
        """Test creating a new superuser."""

        email = 'test@gmail.com'
        password = '1234abcd'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation."""
        tag = models.Tag.objects.create(
            user=simple_user(),
            name='Test_Tag'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation."""
        ingredient = models.Ingredient.objects.create(
            user=simple_user(),
            name='TestIngredient'
        )

        self.assertEqual(str(ingredient), ingredient.name)
