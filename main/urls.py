from django.urls import path

from main.json import get_network_devices, save_all_devices, update_device_status, get_network_allow_devices, \
    get_network_deny_devices
from main.views import all_device, allow_devices, deny_devices, system_role, hemis_role

views_urlpatterns = [
    path('all_device', all_device, name='all_device'),
    path('allow_devices', allow_devices, name='allow_devices'),
    path('deny_devices', deny_devices, name='deny_devices'),
    path('system_role', system_role, name='system_role'),
    path('hemis_role', hemis_role, name='hemis_role'),

]

json_patterns = [
    path('device_list', get_network_devices, name='device_list'),
    path('allow_device_list', get_network_allow_devices, name='allow_device_list'),
    path('deny_device_list', get_network_deny_devices, name='deny_device_list'),
    path('save_all_devices', save_all_devices, name='save_all_devices'),
    path('update_device_status', update_device_status, name='update_device_status'),
]
urlpatterns =views_urlpatterns + json_patterns