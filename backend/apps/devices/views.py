from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Device
from .serializers import DeviceSerializer

# Create your views here.

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['device_type', 'status', 'operating_system']
    search_fields = ['name', 'hostname', 'ip_address', 'serial_number', 'notes']
    ordering_fields = ['name', 'last_seen', 'created_at']
    ordering = ['-last_seen']  # Default ordering

    def get_queryset(self):
        """
        This view should return a list of all devices
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return Device.objects.all()
        return Device.objects.filter(owner=user)
