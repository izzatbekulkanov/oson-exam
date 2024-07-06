from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import NetworkDevice


# Create your views here.


@login_required
def employee_dashboard(request):
    return render(request, 'pages/index.html')


def dashboard(request):
    tasdiqlangan_devices = NetworkDevice.objects.filter(status='Tasdiqlangan')
    context = {'tasdiqlangan_devices': tasdiqlangan_devices}
    return render(request, 'landing/content.html', context)


@login_required
def api_key(request):
    return render(request, 'pages/HEMIS/api_key.html')

@login_required
def data_hemis(request):
    return render(request, 'pages/HEMIS/data_hemis.html')
