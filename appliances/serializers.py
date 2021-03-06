from pyexpat import model
from rest_framework import serializers
from .models import Appliance, Brand, Category, Historic, Problem, Solution, Symptom


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ["id", "model", "brand", "category"]


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "name", "description"]


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "name", "description", "solutions"]


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ["id", "name", "description", "causes"]


class HistoricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historic
        fields = ["id", "appliance", "symptoms", "problems", "solutions", "org", "completed"]
