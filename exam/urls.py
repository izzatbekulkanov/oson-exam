from django.urls import path
from exam.views import employee_dashboard, dashboard

views_urlpatterns = [
    path('employee_dashboard', employee_dashboard, name='employee_dashboard'),
    path('', dashboard, name='landing_dashboard'),
]


urlpatterns =views_urlpatterns