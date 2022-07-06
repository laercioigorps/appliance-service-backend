from functools import partial
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView

from appliances.models import Historic
from profiles.models import Address, Customer
from profiles.permissions import IsCustomerOwner
from profiles.serializers import AddressSerializer, CustomerSerializer
from service.permissions import IsServiceOwner
from .models import Service
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class ServiceListView(APIView):

    permission_classes = [IsAuthenticated]

    class ServiceListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            fields = "__all__"
            depth = 2

    def get(self, request):
        services = Service.objects.filter(owner=request.user.profile.org)
        serializer = self.ServiceListSerializer(services, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        org = request.user.profile.org
        service = Service.objects.create(
            owner=org, historic=Historic.objects.create(org=org)
        )
        serializer = self.ServiceListSerializer(service)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ServiceDetailView(APIView):

    permission_classes = [IsAuthenticated, IsServiceOwner]

    class ServiceDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            fields = "__all__"
            depth = 2

    class ServiceDetailEditSerializer(serializers.ModelSerializer):

        address = AddressSerializer

        class Meta:
            model = Service
            fields = "__all__"

    def get(self, request, service_pk):
        service = get_object_or_404(Service, pk=service_pk)
        self.check_object_permissions(request, service)
        serializer = self.ServiceDetailSerializer(service)
        return Response(data=serializer.data)

    def put(self, request, service_pk):
        service = Service.objects.get(pk=service_pk)
        self.check_object_permissions(request, service)
        serializer = self.ServiceDetailEditSerializer(
            service, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerServiceListView(APIView):

    permission_classes = [IsAuthenticated, IsCustomerOwner]

    class ServiceListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            fields = "__all__"
            depth = 1

    def post(self, request, customer_pk):
        customer = get_object_or_404(Customer, pk=customer_pk)
        self.check_object_permissions(request, customer)
        org = request.user.profile.org
        service = Service.objects.create(
            owner=org, historic=Historic.objects.create(org=org), customer=customer
        )
        serializer = self.ServiceListSerializer(service)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
