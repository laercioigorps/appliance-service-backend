from pyexpat import model
from rest_framework import serializers
from .models import Appliance, Brand, Category, Problem, Solution, Symptom


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ["model", "brand", "category"]


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["name", "description"]


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["name", "description", "solutions"]


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ["name", "description", "causes"]
