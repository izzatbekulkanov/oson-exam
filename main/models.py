from django.db import models

class NetworkDevice(models.Model):
    STATUS_CHOICES = (
        ('Tasdiqlangan', 'Tasdiqlangan'),
        ('Tasdiqlanmagan', 'Tasdiqlanmagan'),
        ('Ta\'qiqlangan', 'Ta\'qiqlangan'),
    )

    ip_address = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17)
    manufacturer = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    user_name = models.CharField(max_length=255)  # Foydalanuvchi nomi
    device_name = models.CharField(max_length=255)  # Qurilma nomi

    def __str__(self):
        return f"{self.ip_address} - {self.mac_address} ({self.manufacturer})"