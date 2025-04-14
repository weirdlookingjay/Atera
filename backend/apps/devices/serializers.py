from rest_framework import serializers
from .models import Device, DeviceSpecification


class DeviceSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSpecification
        fields = [
            'cpu', 'ram_gb', 'storage_gb', 'gpu',
            'screen_size', 'battery_health', 'additional_specs'
        ]


class DeviceSerializer(serializers.ModelSerializer):
    specifications = DeviceSpecificationSerializer(required=False)
    device_type_display = serializers.CharField(source='get_device_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'device_type', 'device_type_display',
            'status', 'status_display', 'ip_address', 'mac_address',
            'hostname', 'operating_system', 'os_version',
            'manufacturer', 'model', 'serial_number',
            'last_seen', 'created_at', 'updated_at',
            'owner', 'notes', 'specifications'
        ]
        read_only_fields = ['last_seen', 'created_at', 'updated_at']

    def create(self, validated_data):
        specifications_data = validated_data.pop('specifications', None)
        device = Device.objects.create(**validated_data)
        
        if specifications_data:
            DeviceSpecification.objects.create(device=device, **specifications_data)
        
        return device

    def update(self, instance, validated_data):
        specifications_data = validated_data.pop('specifications', None)
        
        # Update device fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or create specifications
        if specifications_data:
            if hasattr(instance, 'specifications'):
                for attr, value in specifications_data.items():
                    setattr(instance.specifications, attr, value)
                instance.specifications.save()
            else:
                DeviceSpecification.objects.create(device=instance, **specifications_data)
        
        return instance
