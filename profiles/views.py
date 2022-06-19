from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, APIView
from profiles.models import Address, Customer
from profiles.serializers import AddressSerializer, CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomerOwner

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


class CustomerDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


""" @api_view(["POST"])
@permission_classes([IsAuthenticated, IsCustomerOwner])
def customer_address_list_view(request, pk, format=None):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not customer.has_object_permission(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == "POST":
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            address = serializer.instance
            customer.address.add(address)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED) """


class CustomerAddressListView(APIView):

    permission_classes = [IsAuthenticated, IsCustomerOwner]

    def post(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        self.check_object_permissions(request, customer)
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            address = serializer.instance
            customer.address.add(address)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        self.check_object_permissions(request, customer)
        address = Address.objects.filter(customer__pk=pk)
        serializer = AddressSerializer(address, many=True)
        return Response(data=serializer.data)
