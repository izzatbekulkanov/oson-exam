# log/admin.py for admin interface integration
from django.contrib import admin
from .models import LogEntry  # Import LogEntry model

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'message', 'user_full_name', 'browser_name', 'mac_address', 'device_name', 'global_ip', 'location')
    list_filter = ('level',)
    search_fields = ('message', 'user_full_name', 'global_ip')

admin.site.register(LogEntry, LogEntryAdmin)