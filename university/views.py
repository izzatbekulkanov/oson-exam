from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def university_dashboard(request):
    return render(request, 'app/university/dashboard.html')

@login_required
def university_data(request):
    return render(request, 'applications/university/updateData/updateData.html')

@login_required
def api_token_view(request):
    return render(request, 'applications/university/apiToken/apiToken.html')
