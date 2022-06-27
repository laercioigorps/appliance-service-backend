from django.shortcuts import render
from rest_framework.views import APIView
from .models import Service
from rest_framework import serializers
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
