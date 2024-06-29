from django.urls import path
from exam.views import employee_dashboard, dashboard, settings_log, api_key

views_urlpatterns = [
    path('employee_dashboard', employee_dashboard, name='employee_dashboard'),
    path('settings_log', settings_log, name='settings_log'),
    path('api_key', api_key, name='api_key'),
    path('', dashboard, name='landing_dashboard'),
]


urlpatterns =views_urlpatterns