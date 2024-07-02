from django.contrib import admin
from .models import NetworkDevice

class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'mac_address', 'manufacturer', 'status', 'user_name', 'device_name')
    list_filter = ('status',)
    search_fields = ('ip_address', 'mac_address', 'manufacturer', 'user_name', 'device_name')
    list_per_page = 20

admin.site.register(NetworkDevice, NetworkDeviceAdmin)