from django.http import JsonResponse
from .utils import get_network_devices

def device_list(request):
    devices = get_network_devices()
    return JsonResponse({'devices': devices})