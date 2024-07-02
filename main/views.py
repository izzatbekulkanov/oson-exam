from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def all_device(request):
    return render(request, 'pages/settings/devices.html')