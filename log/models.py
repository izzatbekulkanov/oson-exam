# log/models.py
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20)
    message = models.TextField()
    user_full_name = models.CharField(max_length=255, blank=True, null=True)
    browser_name = models.CharField(max_length=100, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)
    global_ip = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.timestamp} - {self.level}: {self.message}'