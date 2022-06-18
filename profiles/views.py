from pickle import NONE
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from profiles.models import Customer
from profiles.serializers import AddressSerializer, CustomerSerializer
from rest_framework.permissions import IsAuthenticated

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
    if request.method == "GET":
        customer_by_org = Customer.objects.filter(owner=request.user.profile.org)
        serializer = CustomerSerializer(customer_by_org, many=True)
        return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer_address_list_view(request, pk, format=None):
    customer = Customer.objects.get(pk=pk)
    if not customer.has_object_permission(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == "POST":
        serializer = AddressSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            address = serializer.instance
            customer.address.add(address)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            
