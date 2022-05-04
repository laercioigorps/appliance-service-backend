from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from profiles.models import Customer
from profiles.serializers import CustomerSerializer

# Create your views here.
@api_view(["GET", "POST"])
def customer_list_view(request, format=None):
    if request.method == "POST":
        data = request.data
        data["owner"] = request.user.profile.org.id
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user.profile.org)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
