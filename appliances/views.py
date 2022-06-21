from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ApplianceSerializer, BrandSerializer, CategorySerializer, SolutionSerializer
from .models import Appliance, Brand, Category, Solution

# Create your views here.


class BrandListView(APIView):

    def get(self, request, format=None):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(data = serializer.data)


class CategoryListView(APIView):

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data = serializer.data)

class ApplianceListView(APIView):

    def get(self, request, format=None):
        appliances = Appliance.objects.all()
        serializer = ApplianceSerializer(appliances, many=True)
        return Response(data = serializer.data)


class SolutionListView(APIView):

    def get(self, request, format=None):
        solutions = Solution.objects.all()
        serializer = SolutionSerializer(solutions, many=True)
        return Response(data = serializer.data)