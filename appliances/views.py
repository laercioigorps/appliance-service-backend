from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BrandSerializer
from .models import Brand

# Create your views here.


class BrandListView(APIView):

    def get(self, request, format=None):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(data = serializer.data)