from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def settings_log(request):
    return render(request, 'pages/settings/logs.html')