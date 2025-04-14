from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Device(models.Model):
    DEVICE_TYPES = [
        ('WORKSTATION', 'Workstation'),
        ('SERVER', 'Server'),
        ('LAPTOP', 'Laptop'),
        ('NETWORK', 'Network Device'),
        ('MOBILE', 'Mobile Device'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
        ('MAINTENANCE', 'Maintenance'),
        ('UNKNOWN', 'Unknown'),
    ]

    name = models.CharField(_('device name'), max_length=255)
    device_type = models.CharField(_('device type'), max_length=20, choices=DEVICE_TYPES)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='UNKNOWN')
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    mac_address = models.CharField(_('MAC address'), max_length=17, blank=True)
    hostname = models.CharField(_('hostname'), max_length=255, blank=True)
    operating_system = models.CharField(_('operating system'), max_length=100, blank=True)
    os_version = models.CharField(_('OS version'), max_length=50, blank=True)
    manufacturer = models.CharField(_('manufacturer'), max_length=100, blank=True)
    model = models.CharField(_('model'), max_length=100, blank=True)
    serial_number = models.CharField(_('serial number'), max_length=100, blank=True)
    last_seen = models.DateTimeField(_('last seen'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_devices'
    )
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        ordering = ['-last_seen']

    def __str__(self):
        return f"{self.name} ({self.get_device_type_display()})"


class DeviceSpecification(models.Model):
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        related_name='specifications'
    )
    cpu = models.CharField(_('CPU'), max_length=100, blank=True)
    ram_gb = models.PositiveIntegerField(_('RAM (GB)'), null=True, blank=True)
    storage_gb = models.PositiveIntegerField(_('Storage (GB)'), null=True, blank=True)
    gpu = models.CharField(_('GPU'), max_length=100, blank=True)
    screen_size = models.CharField(_('screen size'), max_length=50, blank=True)
    battery_health = models.CharField(_('battery health'), max_length=50, blank=True)
    additional_specs = models.JSONField(_('additional specifications'), default=dict, blank=True)

    class Meta:
        verbose_name = _('device specification')
        verbose_name_plural = _('device specifications')

    def __str__(self):
        return f"Specs for {self.device.name}"
