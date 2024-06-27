from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


@login_required
def employee_dashboard(request):
    return render(request, 'pages/index.html')

@login_required
def student_dashboard(request):
    return render(request, 'pages/index.html')

@login_required
def dashboard(request):
    return render(request, 'landing/content.html')