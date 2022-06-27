from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView

from appliances.models import Historic
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
            depth = 1

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

    permission_classes = [IsAuthenticated]

    class ServiceDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            fields = "__all__"
            depth = 1

    def get(self, request, service_pk):
        service = get_object_or_404(Service, pk=service_pk)
        serializer = self.ServiceDetailSerializer(service)
        return Response(data=serializer.data)
