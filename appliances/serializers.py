from pyexpat import model
from rest_framework import serializers
from .models import Brand, Category


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
