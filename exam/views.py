from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


@login_required
def employee_dashboard(request):
    return render(request, 'pages/index.html')


def dashboard(request):
    return render(request, 'landing/content.html')


@login_required
def api_key(request):
    return render(request, 'pages/HEMIS/api_key.html')
