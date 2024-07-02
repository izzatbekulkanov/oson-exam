from django.urls import path

from main.json import get_network_devices, save_all_devices, update_device_status
from main.views import all_device

views_urlpatterns = [
    path('all_device', all_device, name='all_device'),

]

json_patterns = [
    path('device_list', get_network_devices, name='device_list'),
    path('save_all_devices', save_all_devices, name='save_all_devices'),
    path('update_device_status', update_device_status, name='update_device_status'),
]
urlpatterns =views_urlpatterns + json_patterns