from django.urls import path

from exam.json import device_list
from exam.views import employee_dashboard, dashboard, settings_log, api_key

views_urlpatterns = [
    path('employee_dashboard', employee_dashboard, name='employee_dashboard'),
    path('settings_log', settings_log, name='settings_log'),
    path('api_key', api_key, name='api_key'),
    path('device_list', device_list, name='device_list'),
    path('', dashboard, name='landing_dashboard'),
]


urlpatterns =views_urlpatterns