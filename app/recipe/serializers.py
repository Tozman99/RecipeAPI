from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient object"""

    class Meta:
        
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id", )

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""

    ingredients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ["title", "time_minutes", "price", "user", "link", "tags", "ingredients"]


class RecipeDetailSerializer(RecipeSerializer):
    # we inherit from RecipeSerializer so our meta class has been already created 
    # thoses attr in the meta class are used 

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
