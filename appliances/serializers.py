from pyexpat import model
from rest_framework import serializers
from .models import Brand, Category, Problem, Solution


class BrandSerializer(serializers.Serializer):
    class Meta:
        model = Brand
        fields = ["name"]


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ["name"]


class ApplianceSerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ["model", "brand", "category"]


class SolutionSerializer(serializers.Serializer):
    class Meta:
        model = Solution
        fields = ["name", "description"]


class ProblemSerializer(serializers.Serializer):
    class Meta:
        model = Problem
        fields = ["name", "description", "solutions"]
