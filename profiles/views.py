from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, APIView
from core.utils.utils import concatenateLists, getDisctionaryOfLists
from profiles.models import Address, Customer
from profiles.serializers import AddressSerializer, CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAddressOwner, IsCustomerOwner
from django.db.models import Count
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.


class CustomerListView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        data["owner"] = request.user.profile.org.id
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user.profile.org)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        customer_by_org = Customer.objects.filter(owner=request.user.profile.org)
        limitPagination = LimitOffsetPagination()
        result_page = limitPagination.paginate_queryset(customer_by_org, request)
        serializer = CustomerSerializer(result_page, many=True)
        return Response(
            {
                "results": serializer.data,
                "next": limitPagination.get_next_link(),
                "previous": limitPagination.get_previous_link(),
            }
        )


class CustomerDetailView(APIView):

    permission_classes = [IsAuthenticated, IsCustomerOwner]

    def get(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        self.check_object_permissions(request, customer)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = Customer.objects.get(pk=pk)
        self.check_object_permissions(request, customer)
        customer.delete()
        return Response(status=status.HTTP_200_OK)


class CustomerHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        customerTotalCount = Customer.objects.filter(
            owner=request.user.profile.org
        ).count()
        customers = (
            Customer.objects.filter(owner=request.user.profile.org)
            .values("created_at__month", "created_at__year")
            .annotate(count=Count("created_at__month"))
            .order_by("created_at__year", "created_at__month")
        )

        dict = getDisctionaryOfLists(customers)
        data = []
        labels = concatenateLists(
            dict["created_at__month"], dict["created_at__year"], "-"
        )
        return Response(
            {"data": dict["count"], "labels": labels, "total": customerTotalCount}
        )


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
            customer.addresses.add(address)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        self.check_object_permissions(request, customer)
        address = Address.objects.filter(customer__pk=pk)
        serializer = AddressSerializer(address, many=True)
        return Response(data=serializer.data)


class CustomerAddressDetailView(APIView):

    permission_classes = [IsAuthenticated, IsAddressOwner]

    def get(self, request, pk, address_pk):
        address = get_object_or_404(Address, pk=address_pk)
        self.check_object_permissions(request, address)
        serializer = AddressSerializer(address)
        return Response(data=serializer.data)

    def put(self, request, pk, address_pk):
        address = get_object_or_404(Address, pk=address_pk)
        self.check_object_permissions(request, address)
        serializer = AddressSerializer(address, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, address_pk):
        address = get_object_or_404(Address, pk=address_pk)
        self.check_object_permissions(request, address)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
