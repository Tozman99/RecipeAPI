from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers

class BaseRecipeAttr(viewsets.GenericViewSet, 
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """This class is created for refactoring the Tag and ingredients viewsets
        It gathers all duplicate code from those two classes"""
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get queryset from queryset"""
        # we add the get_queryset method cause queryset is used for having all queryset
        # Here we filter those queryset in order to get tags that user has 
        return self.queryset.filter(user=self.request.user).order_by("-name")
    
    def perform_create(self, serializer):
        """Create a new object it can be either tag or ingredient"""
        # we don;t need to add Tag name cause the user provides it 
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttr):
    """Manage tags in the database"""
    
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    """Manage ingredients in the db """

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Return filtered queryset based on user"""
        return Recipe.objects.filter(user=self.request.user)

