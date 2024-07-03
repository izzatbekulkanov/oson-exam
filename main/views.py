from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def all_device(request):
    return render(request, 'pages/settings/devices.html')

@login_required
def allow_devices(request):
    return render(request, 'pages/settings/allow_devices.html')

@login_required
def deny_devices(request):
    return render(request, 'pages/settings/deny_devices.html')

@login_required
def system_role(request):
    return render(request, 'pages/administrator/system_role.html')

@login_required
def hemis_role(request):
    return render(request, 'pages/administrator/hemis_role.html')