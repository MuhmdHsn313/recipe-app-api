from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeArrtView(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """The base class of all recipe attributes."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return the object for specific user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new attr."""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeArrtView):
    """Manage tags in the DB."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeArrtView):
    """Manage ingredient in the DB."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
