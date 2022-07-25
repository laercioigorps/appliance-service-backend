from datetime import date, timedelta
from functools import partial
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView

from appliances.models import Historic
from profiles.models import Address, Customer
from profiles.permissions import IsCustomerOwner
from profiles.serializers import AddressSerializer, CustomerSerializer
from service.permissions import IsServiceOwner
from .models import Service, Status
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from core.utils.utils import concatenateLists, getDisctionaryOfLists


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
            serviceStatus = serializer.validated_data.get("status")
            if serviceStatus and serviceStatus.is_conclusive:
                serializer.save(end_date=date.today())
            else:
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


class ServiceHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        serviceHistory = (
            Service.objects.filter(owner=request.user.profile.org)
            .filter(end_date__isnull=False)
            .values("end_date__month", "end_date__year")
            .annotate(Sum("price"), Count("end_date__month"))
            .order_by("end_date__year", "end_date__month")
        )

        dict = getDisctionaryOfLists(serviceHistory)
        labels = concatenateLists(dict["end_date__month"], dict["end_date__year"], "-")
        return Response(
            {
                "incomeHistoryData": dict["price__sum"],
                "incomeHistoryLabels": labels,
                "serviceCountHistoryData": dict["end_date__month__count"],
            }
        )


class StatusListView(APIView):
    class StatusListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Status
            fields = ["id", "name", "description", "is_active", "is_conclusive"]

    def get(self, request, format=None):
        statuses = Status.objects.all()
        serializer = self.StatusListSerializer(statuses, many=True)
        return Response(data=serializer.data)


class ServiceByStatusView(APIView):
    def get(self, request, days, format=None):
        servicesByStatus = (
            Service.objects.filter(owner=request.user.profile.org)
            .filter(start_date__gte=date.today() - timedelta(days=days))
            .order_by("status__id")
            .values("status__name")
            .annotate(Count("status"))
        )
        dict = getDisctionaryOfLists(servicesByStatus)

        return Response(
            {
                "data": dict["status__count"],
                "labels": dict["status__name"],
            }
        )
